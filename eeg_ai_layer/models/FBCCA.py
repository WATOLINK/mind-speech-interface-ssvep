import numpy as np
from sklearn.cross_decomposition import CCA
from sklearn.metrics import confusion_matrix, accuracy_score
from typing import List
from eeg_ai_layer.models.utils import filterbank, iir_notch_filter
from scipy.stats import pearsonr
from tqdm import trange


class FBCCA:
    """An FBCCA model."""

    def __init__(self, args):
        self.frequencies = args.frequencies  # [0.0, 12.75, 14.75, 11.75, 10.25]
        self.cca_frequencies = sorted(args.frequencies)
        if self.cca_frequencies[0] == 0.0:
            self.cca_frequencies = self.cca_frequencies[1:]
        print(self.cca_frequencies)
        self.components = args.components
        self.cca = CCA(n_components=self.components)
        self.duration = int(args.window_length * args.sample_rate)
        self.sample_rate = args.sample_rate
        self.quality_factors = 30.0
        self.power_line_frequency = 60
        self.frequency_bands = args.frequency_bands if "frequency_bands" in args else 10
        self.harmonics = args.harmonics if "harmonics" in args else 3
        self.fb_coefs = np.power(np.arange(1, self.frequency_bands + 1), -1.25) + 0.25
        self.verbose = args.verbose
        # TODO: Rewrite this later
        self.cca_frequencies = None
        self.reference_templates = self.create_reference_templates(frequencies=self.frequencies)
        self.freq2label = {freq: idx for idx, freq in enumerate(self.frequencies)}

    def create_reference_templates(self, frequencies: List):
        """
        Create reference signals for CCA.

        Args:
            frequencies: The frequencies (hz) for which to create reference signals

        Returns:
            An array of reference signals
        """
        self.frequencies = sorted(frequencies)
        self.cca_frequencies = [freq for freq in sorted(frequencies) if freq != 0]
        reference_templates = np.zeros((len(self.cca_frequencies), 2 * self.harmonics, self.duration))
        for freq_idx in range(len(self.cca_frequencies)):
            freq = self.cca_frequencies[freq_idx]
            reference_template = []
            for harmonic in range(1, self.harmonics + 1):
                reference_template.extend(self.get_reference_signals(self.duration, harmonic * freq, self.sample_rate))
            reference_templates[freq_idx] = np.array(reference_template)
        return np.array(reference_templates, dtype='float64')

    def get_reference_signals(self, data_len, target_freq, sampling_rate):
        reference_signals = []
        t = np.arange(0, (data_len / sampling_rate), step=1.0 / sampling_rate)
        reference_signals.append(np.sin(np.pi * 2 * target_freq * t))
        reference_signals.append(np.cos(np.pi * 2 * target_freq * t))
        # TODO: why bother with multiplying by 4 here
        # reference_signals.append(np.sin(np.pi * 4 * target_freq * t))
        # reference_signals.append(np.cos(np.pi * 4 * target_freq * t))
        reference_signals = np.array(reference_signals)
        return reference_signals

    def prepare(self, data):
        """
        Prepare data for prediction. To be used in online context.

        Args:
            data: Data from a remote client. (sample_rate, num_channels)

        Returns:
            Prepared data for prediction
        """
        return iir_notch_filter(data=data,
                                f0=self.power_line_frequency,
                                quality_factor=self.quality_factors,
                                sample_rate=self.sample_rate)

    def predict(self, data: np.ndarray):
        """
        Make a prediction for the main frequency each signal using FBCCA.

        Args:
            signals: The input ndarray of signals

        Returns:
            Correlations to each of the reference signals
        """

        cca = CCA(n_components=1)  # initilize CCA

        # result matrix
        r = np.zeros((self.frequency_bands, len(self.cca_frequencies)))
        results = np.zeros(data.shape[0])
        signal_range = range(data.shape[0])
        if self.verbose:
            signal_range = trange(data.shape[0])
        for segment in signal_range:
            for frequency_band in range(self.frequency_bands):
                segment_frequency_bank = filterbank(data[segment].T, self.sample_rate, frequency_band)
                for frequ in range(len(self.cca_frequencies)):
                    refdata = np.squeeze(self.reference_templates[frequ, :, :])  # pick corresponding freq target reference signal
                    test_C, ref_C = cca.fit_transform(segment_frequency_bank.T, refdata.T)
                    r_tmp, _ = pearsonr(np.squeeze(test_C), np.squeeze(ref_C))
                    r[frequency_band, frequ] = r_tmp
            rho = np.dot(self.fb_coefs, r)  # weighted sum of r from all different filter banks' result
            tau = np.argmax(rho)  # get maximum from the target as the final predict (get the index)
            results[segment] = tau  # index indicate the maximum(most possible) target
        return results

    def convert_index_to_frequency(self, predictions: np.array):
        return [self.frequencies[pred] for pred in predictions]

    def test(self, hparams, test_data, test_labels):
        """
        Test the FBCCA model

        Args:
            hparams: hyperparams
            test_data: test data
            test_labels: labels for each data example

        Returns:
            Accuracy metrics. If the verbose param is specified, a confusion matrix is returned as well.
        """
        test_data = np.array(test_data)
        test_data = self.prepare(data=test_data.T).T
        idx_labels = [self.freq2label[label] for label in test_labels]
        predictions = self.predict(data=test_data)
        if self.frequencies[0] == 0:
            predictions = [pred + 1 for pred in predictions]
        cca_accuracy = accuracy_score(y_true=idx_labels, y_pred=predictions)
        metrics = {'test_cca_accuracy': cca_accuracy}
        if hparams.verbose:
            cca_confusion_matrix = confusion_matrix(idx_labels, predictions)
            metrics['test_cca_confusion_matrix'] = cca_confusion_matrix
        return metrics
