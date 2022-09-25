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
        self.components = args.components
        self.cca = CCA(n_components=self.components)
        self.duration = args.window_length * args.sample_rate
        self.sample_rate = args.sample_rate
        self.quality_factors = 30.0
        self.power_line_frequency = 60
        self.frequency_bands = args.frequency_bands if "frequency_bands" in args else 10
        self.harmonics = args.harmonics if "harmonics" in args else 3
        self.fb_coefs = np.power(np.arange(1, self.frequency_bands + 1), -1.25) + 0.25

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
        reference_templates = []
        for freq in self.frequencies:
            if freq == 0:
                continue
            for harmonic in range(1, self.harmonics + 1):
                reference_templates.append(self.get_reference_signals(self.duration, harmonic * freq, self.sample_rate))
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
        Make a prediction on some parsed and filtered EEG data.

        Args:
            data: Parsed and filtered EEG data

        Returns:
            Frequency predictions from the CCA and KNN models
        """
        correlations = self.calculate_correlation(data)
        predictions = np.argmax(correlations, axis=1)
        return predictions, correlations

    def convert_index_to_frequency(self, predictions: np.array):
        return [self.frequencies[pred] for pred in predictions]

    def calculate_correlation(self, signals: np.array) -> np.array:
        """
        Find correlation between input `signals` and `reference` signals using CCA.

        Args:
            signals: The input ndarray of signals
            reference: The reference signals

        Returns:
            Correlations to each of the reference signals
        """

        # num_targs, num_chan, num_smpls, num_trials = eeg.shape
        y_ref = self.cca_reference(self.frequencies, self.sample_rate, signals.shape[1], self.harmonics)

        cca = CCA(n_components=1)  # initilize CCA

        # result matrix
        r = np.zeros((self.frequency_bands, len(self.frequencies)))
        results = np.zeros((signals.shape[0], len(self.frequencies)))

        for segment in trange(signals.shape[0]):
            for freq in range(len(self.frequencies)):
                for frequency_band in range(self.frequency_bands):
                    segment_frequency_bank = filterbank(signals[segment].T, self.sample_rate, frequency_band)

                    refdata = np.squeeze(y_ref[freq, :, :])  # pick corresponding freq target reference signal
                    test_C, ref_C = cca.fit_transform(segment_frequency_bank.T, refdata.T)
                    # len(row) = len(observation), len(column) = variables of each observation
                    # number of rows should be the same, so need transpose here
                    # output is the highest correlation linear combination of two sets
                    r_tmp, _ = pearsonr(np.squeeze(test_C),
                                        np.squeeze(ref_C))  # return r and p_value, use np.squeeze to adapt the API
                    r[frequency_band, freq] = r_tmp
                rho = np.dot(self.fb_coefs, r)  # weighted sum of r from all different filter banks' result
                tau = np.argmax(rho)  # get maximum from the target as the final predict (get the index)
                results[segment, freq] = tau  # index indicate the maximum(most possible) target
        return results

    def cca_reference(self, list_freqs, fs, num_smpls, num_harms=3):

        num_freqs = len(list_freqs)
        tidx = np.arange(1, num_smpls + 1) / fs  # time index

        y_ref = np.zeros((num_freqs, 2 * num_harms, num_smpls))
        for freq_i in range(num_freqs):
            tmp = []
            for harm_i in range(1, num_harms + 1):
                stim_freq = list_freqs[freq_i]  # in HZ
                # Sin and Cos
                tmp.extend([np.sin(2 * np.pi * tidx * harm_i * stim_freq),
                            np.cos(2 * np.pi * tidx * harm_i * stim_freq)])
            y_ref[freq_i] = tmp  # 2*num_harms because include both sin and cos

        return y_ref

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
        idx_labels = [self.freq2label[label] for label in test_labels]
        test_data = np.array(test_data)
        predictions, correlations = self.predict(data=test_data)
        if self.frequencies[0] == 0:
            predictions = [pred + 1 for pred in predictions]
        cca_accuracy = accuracy_score(y_true=idx_labels, y_pred=predictions)
        metrics = {'test_cca_accuracy': cca_accuracy}
        if hparams.verbose:
            cca_confusion_matrix = confusion_matrix(idx_labels, predictions)
            metrics['test_cca_confusion_matrix'] = cca_confusion_matrix
        return metrics
