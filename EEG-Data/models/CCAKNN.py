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

# Helper functions
from .ssvep_utils import get_filtered_eeg, get_segmented_epochs
from sklearn.metrics import confusion_matrix

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
    def __init__(self, model_path: os.PathLike, sample_rate: int = 125, window_len: int = 1, shift_len: int = 1, data: pd.DataFrame = None, left_freq: float = 5, right_freq: float = 21, **kwargs):

        self.window_len = window_len
        self.shift_len = shift_len
        self.sample_rate = sample_rate
        self.duration = self.window_len * self.sample_rate

        # possible flicker frequencies shown to the user
        self.flicker_freq = np.array([9.25, 11.25, 13.25, 9.75, 11.75, 13.75, 
                            10.25, 12.25, 14.25, 10.75, 12.75, 14.75])
        # self.flicker_freq = np.arange(left_freq, right_freq)

        self.KNN = self.load_model(model_path)
    
    def load_model(self, model_path: os.PathLike):
        with open(model_path,'rb') as f:
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
        t = np.arange(0, (data_len/(sampling_rate)), step=1.0/(sampling_rate))
        reference_signals.append(np.sin(np.pi*2*target_freq*t))
        reference_signals.append(np.cos(np.pi*2*target_freq*t))
        reference_signals.append(np.sin(np.pi*4*target_freq*t))
        reference_signals.append(np.cos(np.pi*4*target_freq*t))
        reference_signals = np.array(reference_signals)

        return reference_signals

    def calculate_correlation(signals: np.array, reference: np.array, n_components=1):
        """
        Find correlation between input `signals` and `reference` signals using CCA.

        Args:
            signals: The input ndarray of signals
            reference: The reference signals
        """
        cca = CCA(n_components=n_components)
        result = np.zeros(reference.shape[0])
        for timestep in range(reference.shape[0]):
            cca.fit(signals.T, np.squeeze(reference[timestep, :, :]).T)
            Xcorr, Ycorr = cca.transform(signals.T, np.squeeze(reference[timestep, :, :]).T)
            result[timestep] = np.max(np.corrcoef(Xcorr[:, 0], Ycorr[:, 0])[0, 1])
        return result
    