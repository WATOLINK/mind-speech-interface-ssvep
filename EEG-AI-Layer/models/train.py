from argparse import ArgumentParser
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from typing import List
import os

from ssvep_utils import buffer
from Model import load_model
from utils import parse_and_filter_eeg_data, split_trials


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
    parser.add_argument('--neighbors', type=int, default=3, help="The number of neighbors to pass to a KNN")
    parser.add_argument('--no-zero', action="store_true", default=False,
                        help="Whether to train the model on data with no frequency")
    parser.add_argument('--training-data', type=str, help="Filepath for the training data (csv)")
    parser.add_argument('--testing-data', type=str, help="Filepath for the testing data (csv)")
    parser.add_argument('--model-path', type=str, help="Filepath for a trained model", default=None)
    parser.add_argument('--model-type', type=str, default='cca_knn', help="The model architecture to use. i.e. ccaknn")
    parser.add_argument('--output-path', type=str, default=None, help="Where to save the model")
    parser.add_argument('--output-name', type=str, default=None, help="Name to save the model")
    parser.add_argument('--data', type=str, help="Filepath for a dataset. Will perform a train/test split.")
    parser.add_argument('--sample-rate', type=int, default=250, help="Sampling rate (hz)")
    parser.add_argument('--window-len', type=int, default=1, help="Window length for data processing")
    parser.add_argument('--shift-len', type=int, default=1, help="Shift length for data processing")
    parser.add_argument('--lower-freq', type=float, default=5, help="Lower frequency bound for a bandpass filter")
    parser.add_argument('--upper-freq', type=float, default=5, help="Upper frequency bound for a bandpass filter")
    parser.add_argument('--random-state', type=int, default=42, help="Random State")
    return parser.parse_known_args()


def train(model, data: List[pd.DataFrame], labels: List[float]):
    """
    Training function for the model

    Args:
        hparams: Model hyper parameters
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


def join_datasets(data_path):
    try:
        return pd.read_csv(data_path)
    except IsADirectoryError:
        paths = os.listdir(data_path)[1:]
        data = join_datasets(os.path.join(data_path, paths[0]))
        for path in paths[1:]:
            data.append(join_datasets(os.path.join(data_path, path)))
        return data


if __name__ == "__main__":
    parser = ArgumentParser()
    args, _ = get_args(parser)

    model = load_model(**vars(args))

    train_data, test_data = None, None

    if args.data:
        data = join_datasets(args.data)

        # offset 1 for Timestep
        if all(data.iloc[0, 1:].values == 0):
            data.at[1, 'Frequency'] = data.loc[0, 'Frequency']
            data.at[1, 'Color Code'] = data.loc[0, 'Color Code']
            data = data[1:]
        data = parse_and_filter_eeg_data(data, args.sample_rate, 6, 80)
        label_index = sorted(data['Frequency'].dropna().tolist())
        possible_frequencies = list(set(label_index))
        if args.model_type == 'cca_knn':
            model = load_model(hparams=args, model_type=args.model_type, frequencies=possible_frequencies)
        train_data = data.drop(columns=['time', 'Color Code'])
        trials = split_trials(train_data)
        segments = []
        segment_labels = []
        for trial in trials:
            label = trial.iloc[0]['Frequency']
            trial.drop(columns=['Frequency'], inplace=True)
            duration = args.window_len * args.sample_rate
            data_overlap = (args.window_len - args.shift_len) * args.sample_rate
            segs = buffer(trial, duration, data_overlap)
            for seg in segs:
                segments.append(seg)
                segment_labels.append(label)
        seggies = np.arange(len(segment_labels))
        if args.no_zero:
            segments = [segments[ts] for ts in seggies if segment_labels[ts] != 0]
            segment_labels = [segment_labels[ts] for ts in seggies if segment_labels[ts] != 0]
            seggies = np.arange(len(segment_labels))
        train_segs, test_segs = train_test_split(seggies, test_size=0.2, random_state=42)
        train_data, train_labels = [segments[ts] for ts in train_segs], [segment_labels[ts] for ts in train_segs]
        test_data, test_labels = [segments[ts] for ts in test_segs], [segment_labels[ts] for ts in test_segs]

    if args.training_data:
        train_data = pd.read_csv(args.training_data)
        train_data = parse_and_filter_eeg_data(train_data)
        data_path = args.training_data

    if args.testing_data:
        test_data = pd.read_csv(args.testing_data)
        test_data, splits = parse_and_filter_eeg_data(test_data)

    if args.train:
        train_metrics = train(model, train_data, train_labels)

    test_metrics = test(args, model, test_data, test_labels)

    if args.train:
        test_metrics.update(train_metrics)

    if args.verbose:
        print(*[f"{key}:\n{test_metrics[key]}" for key in test_metrics], sep='\n')

    if args.output_path and args.output_name:
        path = os.path.join(args.output_path, args.output_name)
        print(f"saving at {path}")
        os.makedirs(args.output_path, exist_ok=True)
        model.save_model(path)
