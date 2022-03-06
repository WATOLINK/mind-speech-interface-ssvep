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

# Helper functions
from ssvep_utils import get_filtered_eeg, get_segmented_epochs
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
                val = np.max(np.corrcoef(x_corr[:, 0], y_corr[:, 0])[0, 1])
                if not np.isnan(val):
                    result[segment, freq] = val
        self.CCA = cca
        return result
    
    def train(self, hparams, train_data, train_labels):
        self.trained_freqs = np.unique(train_labels).tolist()
        reference_templates = []
        for freq in self.trained_freqs:
            reference_templates.append(self.get_reference_signals(duration, freq, hparams.sample_rate))
        reference_templates = np.array(reference_templates, dtype='float64')
        train_data = np.array(train_data)
        correlations = self.calculate_correlation(train_data, reference_templates)
        correlations = np.array(correlations)

        clf = KNeighborsClassifier(hparams.neighbors)
        clf.fit(correlations, train_labels)
        self.KNN = clf

    def test(self, hparams, test_data, test_labels):
        reference_templates = []
        for freq in self.trained_freqs:
            reference_templates.append(self.get_reference_signals(duration, freq, hparams.sample_rate))
        reference_templates = np.array(reference_templates, dtype='float64')
        test_data = np.array(test_data)

        correlations = self.calculate_correlation(test_data, reference_templates)
        correlations = np.array(correlations)

        predictions = self.KNN.predict(correlations)
        print(f'accuracy: {accuracy_score(test_labels, predictions):.4f}')
        # print(f'precision: {precision_score(test_labels, predictions):.4f}')
        # print(f'recall: {recall_score(test_labels, predictions):.4f}')
        if hparams.verbose:
            print(confusion_matrix(self.trained_freqs, predictions))

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
        data.index = range(data.shape[0])
    return data

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
        # print(f"data:\n{data}")
        labels = data['Frequency'].dropna().tolist()
        train_data = data.drop(columns=['Time', 'Color Code'])
        trials = split_trials(train_data)
        segments = []
        segment_labels = []
        assert all([np.isna(lab) == False for lab in segment_labels])
        for idx, trial in enumerate(trials):
            duration = args.window_len * args.sample_rate
            data_overlap = (args.window_len - args.shift_len) * args.sample_rate
            segs = buffer(trial, duration, data_overlap)
            for seg in segs:
                segments.append(seg)
                segment_labels.append(labels[idx])
        assert len(segments) == len(segment_labels)
        # print(f"trials:\n{trials}")
        split_loc = int(0.8 * len(segments))
        train_data, train_labels = segments[:split_loc], segment_labels[:split_loc]
        test_data, test_labels = segments[split_loc:], segment_labels[split_loc:]
        # train_data, test_data = train_test_split(data, test_size = 0.3, random_state=args.random_state)
        # train_data.to_csv('train_data.csv', index=False)
        # test_data.to_csv('test_data.csv', index=False)

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