import sys
import os
import math
import numpy as np
import argparse
from sklearn.cross_decomposition import CCA
from sklearn.neighbors import KNeighborsClassifier 
import pandas as pd
from joblib import dump, load
import argparse
from sklearn.model_selection import train_test_split
from typing import List
from collections import Counter

# Helper functions
from ssvep_utils import butter_bandpass_filter, buffer, split_trials, parse_eeg
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score


class CCAKNNModel:
    """
    A generic CCA w/ KNN model.

    Known functions:
        - load kNN params
        - make a prediction
        ===
        - save kNN params
        - train
        - test and develop metrics
    """

    def __init__(self, args):
        self.window_len = args.window_len
        self.sample_rate = args.sample_rate
        self.duration = self.window_len * self.sample_rate
        self.trained_freqs = np.array([5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 14.0, 16.0, 18.0, 20.0])
        self.reference_templates = self.create_reference_templates()
    
    def create_reference_templates(self):
        reference_templates = []
        for freq in self.trained_freqs:
            reference_templates.append(self.get_reference_signals(self.duration, freq, self.sample_rate))
        return np.array(reference_templates, dtype='float32')
    
    def load_model(self, model_path: os.PathLike):
        self.KNN = load(model_path)
    
    def save_model(self, filepath):
        dump(self.KNN, filepath)

    def predict(self, data: np.ndarray, verbose: bool = False):        
        correlations = self.calculate_correlation(train_data, self.reference_templates)
        cca_predictions = np.argmax(correlations, axis=1)
        preds = []
        for pred in cca_predictions:
            preds.append(self.trained_freqs[pred])
        correlations = np.array(correlations)
        predictions = self.KNN.predict(correlations)        
        return predictions
        
    def get_reference_signals(self, data_len, target_freq, sampling_rate):
        reference_signals = []
        t = np.arange(0, (data_len/sampling_rate), step=1.0/sampling_rate)
        reference_signals.append(np.sin(np.pi*2*target_freq*t))
        reference_signals.append(np.cos(np.pi*2*target_freq*t))
        reference_signals.append(np.sin(np.pi*4*target_freq*t))
        reference_signals.append(np.cos(np.pi*4*target_freq*t))
        reference_signals = np.array(reference_signals)

        return reference_signals

    def calculate_correlation(self, signals: np.array, reference: np.array, n_components=1) -> np.array:
        """
        Find correlation between input `signals` and `reference` signals using CCA.

        Args:
            signals: The input ndarray of signals
            reference: The reference signals
            n_components: The number of components for CCA.

        Returns:
            Correlations to each of the reference signals
        """

        cca = CCA(n_components=n_components)
        result = np.zeros((signals.shape[0], reference.shape[0]))
        for segment in range(signals.shape[0]):
            for freq in range(reference.shape[0]):
                cca.fit(signals[segment], np.squeeze(reference[freq, :, :]).T)
                x_corr, y_corr = cca.transform(signals[segment], np.squeeze(reference[freq, :, :]).T)
                corr_matrix = np.corrcoef(x_corr[:, 0], y_corr[:, 0])
                result[segment, freq] = corr_matrix[0, 1]
        return result
    
    def train(self, hparams, train_data, train_labels):
        train_data = np.array(train_data)
        correlations = self.calculate_correlation(train_data, self.reference_templates)
        cca_predictions = np.argmax(correlations, axis=1)
        preds = []
        for pred in cca_predictions:
            preds.append(self.trained_freqs[pred])
        correlations = np.array(correlations)
        
        print(f'CCA train accuracy: {accuracy_score(train_labels, preds):.4f}')
        self.KNN = KNeighborsClassifier(hparams.neighbors)
        self.KNN.fit(correlations, train_labels)
        predictions = self.KNN.predict(correlations)
        print(f'kNN train accuracy: {accuracy_score(train_labels, predictions):.4f}')

    def test(self, hparams, test_data, test_labels):
        assert all([tl in self.trained_freqs for tl in test_labels])
        reference_templates = []
        for freq in self.trained_freqs:
            reference_templates.append(self.get_reference_signals(duration, freq, hparams.sample_rate))
        reference_templates = np.array(reference_templates, dtype='float64')
        test_data = np.array(test_data)

        correlations = self.calculate_correlation(test_data, reference_templates)
        cca_predictions = np.argmax(correlations, axis=1)
        cca_preds = []
        for pred in cca_predictions:
            cca_preds.append(self.trained_freqs[pred])
        
        correlations = np.array(correlations)

        knn_predictions = self.KNN.predict(correlations)
        print(f'kNN accuracy: {accuracy_score(test_labels, knn_predictions):.4f}')
        print(f'CCA accuracy: {accuracy_score(test_labels, cca_preds):.4f}')
        if hparams.verbose:
            print("kNN Confusion Matrix")
            print(self.trained_freqs)
            print(confusion_matrix(test_labels, knn_predictions, labels=self.trained_freqs))
            print("CCA Confusion Matrix")
            print(self.trained_freqs)
            print(confusion_matrix(test_labels, cca_preds, labels=self.trained_freqs))

def get_args(parser):
    parser.add_argument('--train', action="store_true", help="Whether to train a model")
    parser.add_argument('--verbose', action="store_true", help="Verbosity. Will print a confusion matrix if set")
    parser.add_argument('--neighbors', type=int, default=15, help="The number of neighbors to pass to a KNN")
    parser.add_argument('--training-data', type=str, help="Filepath for the training data (csv)")
    parser.add_argument('--testing-data', type=str, help="Filepath for the testing data (csv)")
    parser.add_argument('--model-path', type=str, help="Filepath for a trained KNN model")
    parser.add_argument('--data', type=str, help="Filepath for a dataset. Will perform a train/test split.")
    parser.add_argument('--sample-rate', type=int, default=250, help="Sampling rate (hz)")
    parser.add_argument('--window-len', type=int, default=1, help="Window length for data processing")
    parser.add_argument('--shift-len', type=int, default=1, help="Shift length for data processing")
    parser.add_argument('--lower-freq', type=float, default=5, help="Lower frequency bound for a bandpass filter")
    parser.add_argument('--upper-freq', type=float, default=5, help="Upper frequency bound for a bandpass filter")
    parser.add_argument('--random-state', type=int, default=42, help="Random State")
    return parser.parse_args()

def train(hparams, model, data, labels):
    # labels = data['Frequency'].to_numpy().astype('float64')
    # data = data.drop(columns=['Time', 'Frequency', 'Color Code'])
    # data = data.to_numpy().astype('float64')
    model.train(hparams, data, labels)

def test(hparams, model, data, labels):
    model.test(hparams, data, labels)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = get_args(parser)

    model = CCAKNNModel(args)
    if args.model_path:
        model.load_model(args.model_path)
    train_data, test_data = None, None
    
    if args.data:
        data_path = args.data
        data = pd.read_csv(args.data)
        data = parse_eeg(data)
        labels = sorted(data['Frequency'].dropna().tolist())
        possible_frequencies = list(set(labels))
        model.trained_freqs = possible_frequencies
        train_data = data.drop(columns=['Time', 'Color Code'])
        trials = split_trials(train_data)
        segments = []
        segment_labels = []
        assert all([np.isna(lab) == False for lab in segment_labels])
        for label, trial in zip(labels, trials):
            duration = args.window_len * args.sample_rate
            data_overlap = (args.window_len - args.shift_len) * args.sample_rate
            segs = buffer(trial, duration, data_overlap)
            for seg in segs:
                segments.append(seg)
                segment_labels.append(label)
        seggies = np.arange(len(segment_labels))
        train_segs, test_segs = train_test_split(seggies, test_size=0.2, random_state=42)
        assert len(segments) == len(segment_labels)
        train_data, train_labels = [segments[ts] for ts in train_segs], [segment_labels[ts] for ts in train_segs]
        test_data, test_labels = [segments[ts] for ts in test_segs], [segment_labels[ts] for ts in test_segs]

    if args.training_data:
        train_data = pd.read_csv(args.training_data)
        train_data = parse_eeg(train_data)
        data_path = args.training_data

    if args.testing_data:
        test_data = pd.read_csv(args.testing_data)
        test_data, splits = parse_eeg(test_data)

    if args.train:        
        train(args, model, train_data, train_labels)
        model_save_path = data_path.split("/")[-1][:-4] + '.model'
        print(f"saving at {model_save_path}")
        model.save_model(model_save_path)
    
    test(args, model, test_data, test_labels)