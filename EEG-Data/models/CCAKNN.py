import sys
import os
import math
import numpy as np
import scipy.io as sio
import argparse
from sklearn.cross_decomposition import CCA
import pickle
import pandas as pd
from joblib import dump, load
import argparse

# Helper functions
from .ssvep_utils import get_filtered_eeg, get_segmented_epochs
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

    def __init__(self):

        # self.window_len = window_len
        # self.shift_len = shift_len
        # self.sample_rate = sample_rate
        # self.duration = self.window_len * self.sample_rate

        # possible flicker frequencies shown to the user
        self.flicker_freq = np.array([9.25, 11.25, 13.25, 9.75, 11.75, 13.75, 
                            10.25, 12.25, 14.25, 10.75, 12.75, 14.75])
        # self.flicker_freq = np.arange(left_freq, right_freq)

        # self.KNN = self.load_model(model_path)
    
    def load_model(self, model_path: os.PathLike):
        with open(model_path, 'rb') as f:
            return pickle.load(f)
    
    def save_model(self, filepath):
        dump(self.KNN, filepath)

    def predict(self, data: np.ndarray):
        reference_templates = []
        for freq in self.flicker_freq:
            reference_templates.append(self.get_reference_signals(self.duration, freq, self.sample_rate))
        reference_templates = np.array(reference_templates, dtype='float32')
        
        filtered_data = get_filtered_eeg(data, 6, 80, 4, self.sample_rate)
        segment = get_segmented_epochs(filtered_data, self.window_len, self.shift_len, self.sample_rate)
        labels, predicted_class, all_coeffs = self.calculate_correlation(segment, reference_templates)
        predictions = self.KNN.predict(all_coeffs)
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
        result = np.zeros(reference.shape[0])
        for timestep in range(reference.shape[0]):
            cca.fit(signals.T, np.squeeze(reference[timestep, :, :]).T)
            x_corr, t_corr = cca.transform(signals.T, np.squeeze(reference[timestep, :, :]).T)
            result[timestep] = np.max(np.corrcoef(x_corr[:, 0], y_corr[:, 0])[0, 1])
        return result
    
    def train(self, hparams, train_data, train_labels):
        """"""
        clf = sklearn.neighbors.KNeighborsClassifier(hparams.neighbors)
        clf.fit(train_data, train_labels)
        self.KNN = clf
    
    def test(self, hparams, test_data, test_labels):
        """"""
        predictions = self.KNN.predict(test_data)
        print(f'accuracy: {accuracy_score(test_labels, predictions):.4f}')
        print(f'precision: {precision_score(test_labels, predictions):.4f}')
        print(f'recall: {recall_score(test_labels, predictions):.4f}')
        if hparams.verbose:
            print(confusion_matrix(test_labels, predictions))

def get_args(parser):
    parser.add_argument('--neighbours', type=int, default=15, help="The number of neighbours to pass to a KNN")
    parser.add_argument('--training-data', type=os.PathLike, help="Filepath for the training data (csv)")
    parser.add_argument('--testing-data', type=os.PathLike, help="Filepath for the testing data (csv)")
    parser.add_argument('--model-path', type=os.PathLike, help="Filepath for a trained KNN model")
    parser.add_argument('--sample-rate', type=int, default=250, help="Sampling rate (hz)")
    parser.add_argument('--window-len', type=int, default=1, help="Window length for data processing")
    parser.add_argument('--shift-len', type=int, default=1, help="Shift length for data processing")
    parser.add_argument('--lower-freq', type=float, default=5, help="Lower frequency bound for a bandpass filter")
    parser.add_argument('--upper-freq', type=float, default=5, help="Upper frequency bound for a bandpass filter")

    return parser.parse_args()

def train(hparams, model):
    train_data = pd.read_csv(hparams.training_data)

    model.train(train_data, train_labels)

def test(hparams, model):
    test_data = pd.read_csv(hparams.testing_data)

    model.test(test_data, test_labels)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args, _ = get_args(parser)

    model = CCAKNNModel()
    if args.model_path:
        model.load_model(args.model_path)
    
    if args.training_data:
        train(args, model)

    if args.testing_data:
        test(args, model)
