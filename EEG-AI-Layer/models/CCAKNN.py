import os
import numpy as np
from sklearn.cross_decomposition import CCA
from sklearn.neighbors import KNeighborsClassifier
from joblib import dump, load
from sklearn.metrics import confusion_matrix, accuracy_score
from typing import List
from ssvep_utils import butter_bandpass_filter


class CCAKNNModel:
    """A generic CCA w/ KNN model."""

    def __init__(self, **kwargs):
        model_path = kwargs.get('model_path', None)
        components = kwargs.get('components', 1)
        neighbors = kwargs.get('neighbors', 3)
        self.cca = CCA(n_components=components)
        self.duration = kwargs.get('window_len', 1) * kwargs.get('sample_rate', 250)
        self.sample_rate = kwargs.get('sample_rate', 250)
        freqs = [0.0, 12.75, 14.75, 11.75, 10.25]
        self.trained_freqs = kwargs.get('frequencies', freqs)
        self.cca_frequencies = None
        self.freq2label = None
        self.reference_templates = None
        if self.trained_freqs:
            self.reference_templates = self.create_reference_templates(frequencies=self.trained_freqs)
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
        return np.array(reference_templates, dtype='float64')

    def get_reference_signals(self, data_len, target_freq, sampling_rate):
        reference_signals = []
        t = np.arange(0, (data_len / sampling_rate), step=1.0 / sampling_rate)
        reference_signals.append(np.sin(np.pi * 2 * target_freq * t))
        reference_signals.append(np.cos(np.pi * 2 * target_freq * t))
        reference_signals.append(np.sin(np.pi * 4 * target_freq * t))
        reference_signals.append(np.cos(np.pi * 4 * target_freq * t))
        reference_signals = np.array(reference_signals)

        return reference_signals

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

    def prepare(self, data):
        """
        Prepare data for prediction. To be used in online context.

        Args:
            data: Data from a remote client. (sample_rate, num_channels)

        Returns:
            Prepared data for prediction
        """
        data = butter_bandpass_filter(data.T, 6, 80, 250, 4).T
        return data[np.newaxis, :]

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
        cca_predictions, correlations = self.cca_predict(data=train_data)
        if self.trained_freqs[0] == 0:
            cca_predictions = [pred + 1 for pred in cca_predictions]
        cca_predictions = np.array(cca_predictions)
        cca_accuracy = accuracy_score(y_true=idx_labels, y_pred=cca_predictions)
        self.knn.fit(correlations, idx_labels)
        predictions = self.knn.predict(correlations)
        knn_accuracy = accuracy_score(y_true=idx_labels, y_pred=predictions)
        return {'train_cca_accuracy': cca_accuracy, 'train_cca_predictions': cca_predictions,
                'train_knn_accuracy': knn_accuracy, 'train_knn_predictions': predictions}

    def test(self, hparams, test_data, test_labels):
        idx_labels = [self.freq2label[label] for label in test_labels]
        test_data = np.array(test_data)
        cca_predictions, correlations = self.cca_predict(data=test_data)
        if self.trained_freqs[0] == 0:
            cca_predictions = [pred + 1 for pred in cca_predictions]
        cca_accuracy = accuracy_score(y_true=idx_labels, y_pred=cca_predictions)
        knn_predictions = self.knn.predict(correlations)
        knn_accuracy = accuracy_score(y_true=idx_labels, y_pred=knn_predictions)
        metrics = {'test_cca_accuracy': cca_accuracy, 'test_knn_accuracy': knn_accuracy}
        if hparams.verbose:
            cca_confusion_matrix = confusion_matrix(idx_labels, cca_predictions)
            metrics['test_cca_confusion_matrix'] = cca_confusion_matrix
            knn_confusion_matrix = confusion_matrix(idx_labels, knn_predictions)
            metrics['test_knn_confusion_matrix'] = knn_confusion_matrix
        return metrics
