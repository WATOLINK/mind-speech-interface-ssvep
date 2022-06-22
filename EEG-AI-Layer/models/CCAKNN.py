import os
import numpy as np
from sklearn.cross_decomposition import CCA
from sklearn.neighbors import KNeighborsClassifier 
from joblib import dump, load
from sklearn.metrics import confusion_matrix, accuracy_score
from typing import List


class CCAKNNModel:
    """A generic CCA w/ KNN model."""

    def __init__(self, model_path = None, **kwargs):
        components = kwargs.get('components', 1)
        neighbors = kwargs.get('neighbors', 3)
        self.cca = CCA(n_components=components)
        if model_path:
            self.load_model(model_path=model_path)
        else:
            self.knn = KNeighborsClassifier(n_neighbors=neighbors)

    def create_reference_templates(self, frequencies: List):
        """
        Create reference signals for CCA.

        Args:
            frequencies: The frequencies (hz) for which to create reference signals

        Returns:
            An array of reference signals
        """
        self.trained_freqs = sorted(frequencies)
        self.cca_frequencies = [freq for freq in sorted(frequencies) if freq != 0]
        self.freq2label = {freq: idx for idx, freq in enumerate(self.trained_freqs)}
        reference_templates = []
        for freq in self.trained_freqs:
            if freq == 0:
                continue
            reference_templates.append(self.get_reference_signals(self.duration, freq, self.sample_rate))
        self.reference_templates = np.array(reference_templates, dtype='float64')

    def load_model(self, model_path: os.PathLike):
        self.knn = load(model_path)
    
    def save_model(self, filepath):
        dump(self.knn, filepath)

    def cca_predict(self, data: np.ndarray):
        """
        Make a prediction using CCA on some parsed and filtered EEG data.

        Args:
            data: Parsed and filtered EEG data

        Returns:
            Frequency predictions from the CCA model
        """
        correlations = self.calculate_correlation(data, self.reference_templates)
        predictions = np.argmax(correlations, axis=1)
        return predictions, correlations

    def predict(self, data: np.ndarray):
        """
        Make a prediction on some parsed and filtered EEG data.

        Args:
            data: Parsed and filtered EEG data

        Returns:
            Frequency predictions from the CCA and KNN models
        """
        predictions, correlations = self.cca_predict(data)
        predictions = self.knn.predict(correlations)
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

    def calculate_correlation(self, signals: np.array, reference: np.array) -> np.array:
        """
        Find correlation between input `signals` and `reference` signals using CCA.

        Args:
            signals: The input ndarray of signals
            reference: The reference signals

        Returns:
            Correlations to each of the reference signals
        """
        result = np.zeros((signals.shape[0], reference.shape[0]))
        for segment in range(signals.shape[0]):
            for freq in range(reference.shape[0]):
                self.cca.fit(signals[segment], np.squeeze(reference[freq, :, :]).T)
                x_corr, y_corr = self.cca.transform(signals[segment], np.squeeze(reference[freq, :, :]).T)
                corr_matrix = np.corrcoef(x_corr[:, 0], y_corr[:, 0])
                result[segment, freq] = corr_matrix[0, 1]
        return result
    
    def train(self, train_data, train_labels):
        idx_labels = [self.freq2label[label] for label in train_labels]
        train_data = np.array(train_data)
        predictions, correlations = self.cca_predict(data=train_data)
        predictions = np.array(predictions)
        print(f'CCA train accuracy: {accuracy_score(y_true=idx_labels, y_pred=predictions):.4f}')
        self.knn.fit(correlations, idx_labels)
        predictions = self.knn.predict(correlations)
        print(f'kNN train accuracy: {accuracy_score(y_true=idx_labels, y_pred=predictions):.4f}')

    def test(self, hparams, test_data, test_labels):
        idx_labels = [self.freq2label[label] for label in test_labels]
        test_data = np.array(test_data)
        cca_predictions, correlations = self.cca_predict(data=test_data)
        knn_predictions = self.knn.predict(correlations)
        print(f'kNN accuracy: {accuracy_score(y_true=idx_labels, y_pred=knn_predictions):.4f}')
        print(f'CCA accuracy: {accuracy_score(y_true=idx_labels, y_pred=cca_predictions):.4f}')
        if hparams.verbose:
            print("kNN Confusion Matrix")
            print(self.trained_freqs)
            print(confusion_matrix(test_labels, knn_predictions, labels=self.trained_freqs))
            print("CCA Confusion Matrix")
            print(self.trained_freqs)
            print(confusion_matrix(test_labels, cca_predictions, labels=self.trained_freqs))
