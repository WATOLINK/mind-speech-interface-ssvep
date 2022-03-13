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
from ssvep_utils import butter_bandpass_filter, get_filtered_eeg, get_segmented_epochs
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
        # possible flicker frequencies shown to the user
        self.trained_freqs = []
        self.flicker_freq = np.array([9.25, 11.25, 13.25, 9.75, 11.75, 13.75, 
                            10.25, 12.25, 14.25, 10.75, 12.75, 14.75])
    
    def load_model(self, model_path: os.PathLike):
        self.KNN = load(model_path)
    
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
        result = np.zeros((signals.shape[0], reference.shape[0]))
        for segment in range(signals.shape[0]):
            for freq in range(reference.shape[0]):
                cca.fit(signals[segment], np.squeeze(reference[freq, :, :]).T)
                x_corr, y_corr = cca.transform(signals[segment], np.squeeze(reference[freq, :, :]).T)
                corr_matrix = np.corrcoef(x_corr[:, 0], y_corr[:, 0])
                result[segment, freq] = corr_matrix[0, 1]
        return result
    
    def train(self, hparams, train_data, train_labels):
        reference_templates = []
        for freq in self.trained_freqs:
            reference_templates.append(self.get_reference_signals(duration, freq, hparams.sample_rate))
        reference_templates = np.array(reference_templates, dtype='float64')
        train_data = np.array(train_data)
        correlations = self.calculate_correlation(train_data, reference_templates)
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
        assert [tl in self.trained_freqs for tl in test_labels]
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

def buffer(data, duration, data_overlap):
    '''
    Returns segmented data based on the provided input window duration and overlap.

    Args:
        data (pd.DataFrame): dataset. 
        duration (int): window length (number of samples).
        data_overlap (int): number of samples of overlap.

    Returns:
        (numpy.ndarray): segmented data of shape (number_of_segments, duration).
    '''
    # TODO: AVOID tossing out the data
    data = data[:-(data.shape[0] % duration)]
    number_segments = int(math.ceil((len(data) - data_overlap)/(duration - data_overlap)))
    temp_buf = [data[i:i + duration] for i in range(0, len(data), (duration - int(data_overlap)))]
    temp_buf[number_segments-1] = np.pad(temp_buf[number_segments-1],
                            (0, duration - temp_buf[number_segments-1].shape[0]),
                            'constant')
    temp_buf = np.array(temp_buf[:number_segments])
    return temp_buf

def split_trials(data) -> List[pd.DataFrame]:
    """
    Segment the data by trial.

    Args:
        data: The EEG data
    
    Returns:
        A list of DataFrames that each contain a trial
    """
    trial_indices = data['Frequency'].dropna().index.sort_values().tolist()
    segmented_data = []
    for idx in range(1, len(trial_indices)):
        data_slice = data[trial_indices[idx - 1]: trial_indices[idx]]
        data_slice['Frequency'] = data_slice['Frequency'].ffill()
        segmented_data.append(data_slice)
    return segmented_data

def parse_eeg(data: pd.DataFrame) -> pd.DataFrame:
    """
    Perform basic parsing on EEG data.

    Args:
        data: The EEG data

    Returns:
        Parsed EEG data
    """
    # offset 1 for Timestep
    if all(data.iloc[0, 1:].values == 0):
        data.at[1, 'Frequency'] = data.loc[0, 'Frequency']
        data.at[1, 'Color Code'] = data.loc[0, 'Color Code']
        data = data[1:]
    datafreqs = data['Frequency'].ffill()
    datafreqs = datafreqs.loc[datafreqs == 0.0]

    data_freqs = data.drop(datafreqs.index)
    
    channel_data = data_freqs.drop(columns=['Time', 'Frequency', 'Color Code'])
    channel_data = channel_data.to_numpy().T
    filtered_data = butter_bandpass_filter(channel_data, 6, 80, 250, 4).T
    df = pd.DataFrame(filtered_data)
    df.columns = [f'CH{i}' for i in range(1, df.shape[1] + 1)]
    df['Time'] = data_freqs['Time']
    df['Frequency'] = data_freqs['Frequency']
    df['Color Code'] = data_freqs['Color Code']
    df.index = np.arange(df.shape[0])
    return df

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

    model = CCAKNNModel()
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