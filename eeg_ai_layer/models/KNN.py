import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from joblib import dump, load
from sklearn.metrics import confusion_matrix, accuracy_score
from typing import List
from eeg_ai_layer.models.FBCCA import FBCCA


class KNN:
    """A KNN model that accepts CCA or FBCCA features as input."""

    def __init__(self, args):
        if hasattr(args, "model_path") and args.model_path:
            self.knn, self.frequencies, self.components = self.load_model(model_path=args.model_path)
        else:
            self.frequencies = [8.25, 8.75, 9.75, 10.75, 11.75, 12.75, 13.75, 14.25]
            if hasattr(args, "frequencies"):
                self.frequencies = args.frequencies
            self.frequencies = args.frequencies  # [0.0, 12.75, 14.75, 11.75, 10.25]
            self.components = args.components
            self.knn = KNeighborsClassifier(n_neighbors=args.neighbors)
        self.duration = int(args.window_length * args.sample_rate)
        self.sample_rate = args.sample_rate
        # CCA Initialization
        self.fbcca = FBCCA(args)
        self.verbose = args.verbose if hasattr(args, "verbose") else False
        self.freq2label = {freq: idx for idx, freq in enumerate(self.frequencies)}

    def prepare(self, data):
        """
        Prepare data for prediction. To be used in online context.

        Args:
            data: Data from a remote client. (sample_rate, num_channels)

        Returns:
            Prepared data for prediction
        """
        prepared = self.fbcca.prepare(data)
        _, correlations = self.fbcca.predict(prepared, self.frequencies)
        return correlations

    def predict(self, correlations: np.ndarray, frequencies: List[float] = None):
        """
        Make a prediction for the main frequency each signal using a KNN, given
        correlations from FBCCA as input.

        Args:
            data: The input data.
            frequencies: An optional subset of frequencies to predict for.
                If none are provided, predicts on the standard frequencies defined in the class.

        Returns:
            Index of frequency in frequencies with the highest correlation.
            Also returns the confidence for each of the correlations
        """
        if frequencies is None:
            frequencies = self.frequencies
        predictions = self.knn.predict(correlations)
        freq2label = {freq: label for label, freq in enumerate(frequencies)}
        final_preds = []
        mapping = [self.freq2label[freq] for freq in frequencies]
        for idx, pred in enumerate(predictions):
            pred_freq = self.frequencies[pred]
            if pred_freq in freq2label:
                final_preds.append(freq2label[pred_freq])
                # print("KNN prediction")
            else:
                relevant_corr = correlations[idx][mapping]
                final_preds.append(np.argmax(relevant_corr))
                # print("FBCCA prediction")
        return final_preds, correlations

    def load_model(self, model_path):
        state = load(model_path)
        return state['knn'], state['frequencies'], state['components']

    def save_model(self, filepath):
        dump({'components': self.components, 'knn': self.knn, 'frequencies': self.frequencies}, filepath)

    def convert_index_to_frequency(self, predictions: np.array, frequencies: List[float] = None):
        if frequencies is None:
            frequencies = self.frequencies
        return [frequencies[pred] for pred in predictions]

    def train(self, train_data, train_labels):
        idx_labels = [self.freq2label[label] for label in train_labels]
        train_data = np.array(train_data)
        correlations = self.prepare(data=train_data)
        self.knn.fit(correlations, idx_labels)
        predictions, _ = self.predict(correlations)
        knn_accuracy = accuracy_score(y_true=idx_labels, y_pred=predictions)
        return {'train_accuracy': knn_accuracy, 'train_predictions': predictions}

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
        correlations = self.prepare(data=test_data)
        idx_labels = [self.freq2label[label] for label in test_labels]
        predictions, _ = self.predict(correlations)
        knn_accuracy = accuracy_score(y_true=idx_labels, y_pred=predictions)
        metrics = {'test_accuracy': knn_accuracy}
        if hparams.verbose:
            fbcca_knn_confusion_matrix = confusion_matrix(idx_labels, predictions)
            metrics['test_confusion_matrix'] = fbcca_knn_confusion_matrix
        return metrics
