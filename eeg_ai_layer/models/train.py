from argparse import ArgumentParser
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, KFold
from typing import List
import os

from eeg_ai_layer.models.ssvep_utils import buffer
from eeg_ai_layer.models.Model import load_model
from eeg_ai_layer.models.utils import parse_and_filter_eeg_data, split_trials


def get_args(parser: ArgumentParser):
    """
    Parse CLI args

    Args:
        parser: The ArgumentParser

    Returns:
        Parsed commandline args
    """
    parser.add_argument('--components', type=int, default=1, help="Number of components for CCA")
    parser.add_argument('--train', action="store_true", help="Whether to train a model")
    parser.add_argument('--verbose', action="store_true", help="Verbosity level. Will print a confusion matrix if set")
    parser.add_argument('--neighbors', type=int, default=4, help="The number of neighbors to pass to a KNN")
    parser.add_argument('--no-zero', action="store_true", default=False, help="Don't train a model on zero frequency")
    parser.add_argument('--splits', default=5, type=int, help="Number of splits for cross validation")
    parser.add_argument('--cross-val', default=False, action="store_true", help="Whether to use cross validation")
    parser.add_argument('--model-path', type=str, help="Filepath for a trained model", default=None)
    parser.add_argument('--model-type', type=str, default='fbcca', help="The model architecture to use. i.e. fbcca")
    parser.add_argument('--output-path', type=str, default=None, help="Where to save the model")
    parser.add_argument('--output-name', type=str, default=None, help="Name to save the model")
    parser.add_argument('--data', type=str, help="Filepath for a dataset. Will perform a train/test split.")
    parser.add_argument('--sample-rate', type=int, default=250, help="Sampling rate (hz)")
    parser.add_argument('--window-length', type=float, default=1, help="Window length for data processing")
    parser.add_argument('--shift-length', type=float, default=1, help="Shift length for data processing")
    parser.add_argument('--lower-freq', type=float, default=7, help="Lower frequency bound for a bandpass filter")
    parser.add_argument('--upper-freq', type=float, default=16, help="Upper frequency bound for a bandpass filter")
    parser.add_argument('--random-state', type=int, default=42, help="Random State")
    return parser.parse_known_args()


def train(model, data: List[pd.DataFrame], labels: List[float]):
    """
    Training function for the model

    Args:
        model: Model instance
        data: Training data
        labels: Labels that correspond to the frequency for the training data

    Returns:
        A trained model
    """
    return model.train(data, labels)


def test(hparams: dict, model, data: List[pd.DataFrame], labels: List[float]):
    """
    Testing function for the model

    Args:
        hparams: Model hyper parameters
        model: Model instance
        data: Testing data
        labels: Labels that correspond to the frequency for the testing data

    Returns:
        Metrics for the tested model
    """
    return model.test(hparams, data, labels)


def join_datasets(data_path: str) -> pd.DataFrame:
    """
    A recursive function to join csvs.

    Args:
        data_path: The root directory for csvs in folders.

    Returns:
        A single dataFrame containing joined data of all csvs.
    """
    try:
        data = pd.read_csv(data_path)
        return data
    except IsADirectoryError:
        paths = [path for path in os.listdir(data_path) if path.endswith(".csv") or os.path.isdir(os.path.join(data_path, path))]
        data = join_datasets(os.path.join(data_path, paths[0]))
        for path in paths[1:]:
            data = data.append(join_datasets(os.path.join(data_path, path)), ignore_index=True)
        return data


def segment_data_from_trials(trials: List, no_zero = False):
    segments = []
    segment_labels = []
    for trial in trials:
        label = trial.iloc[0]['Frequency']
        trial.drop(columns=['Frequency'], inplace=True)
        duration = int(args.window_length * args.sample_rate)
        data_overlap = (args.window_length - args.shift_length) * args.sample_rate
        segs = buffer(trial, duration, data_overlap)
        for seg in segs:
            segments.append(seg)
            segment_labels.append(label)
    if no_zero:
        segments = [segment for idx, segment in enumerate(segments) if segment_labels[idx] != 0]
        segment_labels = [segment_label for idx, segment_label in enumerate(segment_labels) if segment_labels[idx] != 0]
    return segments, segment_labels


def display_metrics(metrics: dict):
    for key in metrics:
        message = f"{key}: {test_metrics[key]}"
        if "confusion_matrix" in key:
            message = f"{key}:\n{test_metrics[key]}"
        print(message)


if __name__ == "__main__":
    parser = ArgumentParser()
    args, _ = get_args(parser)

    segments, segment_labels = None, None

    if args.data:
        data = join_datasets(args.data)
        data.drop(columns=['time', 'Color Code'], inplace=True)

        # offset 1 for Timestep
        if all(data.iloc[0, 1:].values == 0):
            data.at[1, 'Frequency'] = data.loc[0, 'Frequency']
            data = data[1:]
            data.index = np.arange(data.shape[0])

        if args.model_type == "fbcca":
            trials = split_trials(data)
            test_data, test_labels = segment_data_from_trials(trials=trials, no_zero=args.no_zero)
        else:
            train_data = parse_and_filter_eeg_data(data=data, sample_rate=args.sample_rate, lowcut=args.lower_freq,
                                                   highcut=args.upper_freq)
            trials = split_trials(train_data)
            segments, segment_labels = segment_data_from_trials(trials=trials, no_zero=args.no_zero)

    freqs = np.unique(data['Frequency'].dropna().sort_values())
    if args.no_zero:
        freqs = freqs[np.nonzero(freqs)]
    args.__dict__['frequencies'] = freqs
    best_model = None
    best_metrics = {}
    train_accuracies = []
    test_accuracies = []

    if args.train and args.model_type != "fbcca":
        if args.cross_val:
            print(f"Cross validation on {args.splits} splits")
            kf = KFold(n_splits=args.splits)
            kf.get_n_splits(segments)
            for train_index, test_index in kf.split(segments):
                model = load_model(args=args)
                X_train, X_test = [segments[t_idx] for t_idx in train_index], [segments[t_idx] for t_idx in test_index]
                y_train, y_test = [segment_labels[t_idx] for t_idx in train_index], [segment_labels[t_idx] for t_idx in test_index]
                train_metrics = train(model, X_train, y_train)
                train_accuracies.append(train_metrics["train_accuracy"])
                test_metrics = test(args, model, X_test, y_test)
                test_accuracies.append(test_metrics["test_accuracy"])
                display_metrics(test_metrics)
                if test_metrics["test_accuracy"] > best_metrics.get("test_accuracy", 0):
                    best_metrics = test_metrics
                    best_model = model
            if args.verbose:
                train_accuracies = np.array(train_accuracies)
                test_accuracies = np.array(test_accuracies)
                print(f"Avg train accuracy: {np.mean(train_accuracies)}, sd: {np.std(train_accuracies)}",
                      f"Avg test accuracy: {np.mean(test_accuracies)}, sd: {np.std(test_accuracies)}", sep='\n')
                print(f"Best model test accuracy: {best_metrics['test_accuracy']}")
        else:
            model = load_model(args)
            seggies = np.arange(len(segment_labels))
            train_segs, test_segs = train_test_split(seggies, test_size=0.2, random_state=42)
            train_data, train_labels = [segments[ts] for ts in train_segs], [segment_labels[ts] for ts in train_segs]
            test_data, test_labels = [segments[ts] for ts in test_segs], [segment_labels[ts] for ts in test_segs]
            print("Train")
            train_metrics = train(model, train_data, train_labels)
            print("Test")
            test_metrics = test(args, model, test_data, test_labels)
            test_metrics.update(train_metrics)
            if args.verbose:
                display_metrics(test_metrics)

    model = load_model(args)
    if args.train:
        print("Train")
        train(model, segments, segment_labels)
    else:
        print("Test")
        test(args, model, segments, segment_labels)

    if args.output_path and args.output_name:
        path = os.path.join(args.output_path, args.output_name)
        print(f"saving at {path}")
        os.makedirs(args.output_path, exist_ok=True)
        model.save_model(path)
