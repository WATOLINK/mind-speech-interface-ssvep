import argparse
from Model import Model
from CCAKNN import CCAKNNModel
import pandas as pd

def get_args(parser: argparse.ArgumentParser):
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

    model = CCAKNNModel(args)
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
