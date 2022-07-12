import matplotlib.pyplot as plt
import itertools
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
from typing import List
from eeg_ai_layer.models.ssvep_utils import butter_bandpass_filter


def make_confusion_matrix(y_true, y_pred, classes=None, figsize=(10, 10), text_size=15, norm=False, savefig=False):
    """Makes a labelled confusion matrix comparing predictions and ground truth labels.
    If classes is passed, confusion matrix will be labelled, if not, integer class values
    will be used.
    Args:
      y_true: Array of truth labels (must be same shape as y_pred).
      y_pred: Array of predicted labels (must be same shape as y_true).
      classes: Array of class labels (e.g. string form). If `None`, integer labels are used.
      figsize: Size of output figure (default=(10, 10)).
      text_size: Size of output figure text (default=15).
      norm: normalize values or not (default=False).
      savefig: save confusion matrix to file (default=False).

    Returns:
      A labelled confusion matrix plot comparing y_true and y_pred.
    Example usage:
      make_confusion_matrix(y_true=test_labels, # ground truth test labels
                            y_pred=y_preds, # predicted labels
                            classes=class_names, # array of class label names
                            figsize=(15, 15),
                            text_size=10)
    """
    # Create the confustion matrix
    cm = confusion_matrix(y_true, y_pred)
    cm_norm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]  # normalize it
    n_classes = cm.shape[0]  # find the number of classes we're dealing with

    # Plot the figure and make it pretty
    fig, ax = plt.subplots(figsize=figsize)
    cax = ax.matshow(cm, cmap=plt.cm.Blues)  # colors will represent how 'correct' a class is, darker == better
    fig.colorbar(cax)

    # Are there a list of classes?
    if classes:
        labels = classes
    else:
        labels = np.arange(cm.shape[0])

    # Label the axes
    ax.set(title="Confusion Matrix",
           xlabel="Predicted label",
           ylabel="True label",
           xticks=np.arange(n_classes),  # create enough axis slots for each class
           yticks=np.arange(n_classes),
           xticklabels=labels,  # axes will labeled with class names (if they exist) or ints
           yticklabels=labels)

    # Make x-axis labels appear on bottom
    ax.xaxis.set_label_position("bottom")
    ax.xaxis.tick_bottom()

    # Set the threshold for different colors
    threshold = (cm.max() + cm.min()) / 2.

    # Plot the text on each cell
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        if norm:
            plt.text(j, i, f"{cm[i, j]} ({cm_norm[i, j] * 100:.1f}%)",
                     horizontalalignment="center",
                     color="white" if cm[i, j] > threshold else "black",
                     size=text_size)
        else:
            plt.text(j, i, f"{cm[i, j]}",
                     horizontalalignment="center",
                     color="white" if cm[i, j] > threshold else "black",
                     size=text_size)

    # Save the figure to the current working directory
    if savefig:
        fig.savefig("confusion_matrix.png")


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


def parse_and_filter_eeg_data(data: pd.DataFrame, sample_rate: int, lowcut: float, highcut: float) -> pd.DataFrame:
    """
    Perform basic parsing and filter EEG data.

    Args:
        data: The EEG data
        sample_rate: The sampling rate for the EEG data (hz)
        lowcut: Lower frequency
        highcut: Higher frequency

    Returns:
        Parsed + filtered EEG data
    """
    channel_data = data.drop(columns=['time', 'Frequency', 'Color Code'])
    channel_data = channel_data.to_numpy().T
    filtered_data = butter_bandpass_filter(channel_data, lowcut, highcut, sample_rate, 4).T
    df = pd.DataFrame(filtered_data)
    df.columns = [f'CH{i + 1}' for i in range(df.shape[1])]
    df['time'] = data['time']
    df['Frequency'] = data['Frequency']
    df['Color Code'] = data['Color Code']
    df.index = np.arange(df.shape[0])
    return df
