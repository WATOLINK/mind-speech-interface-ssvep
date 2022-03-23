"""
Utilities for CNN based SSVEP Classification
"""
import math
from typing import List
import warnings
import pandas as pd
warnings.filterwarnings('ignore')

import numpy as np
from scipy.signal import butter, filtfilt

def butter_bandpass_filter(data, lowcut, highcut, sample_rate, order):
    '''
    Returns bandpass filtered data between the frequency ranges specified in the input.

    Args:
        data (numpy.ndarray): array of samples. 
        lowcut (float): lower cutoff frequency (Hz).
        highcut (float): lower cutoff frequency (Hz).
        sample_rate (float): sampling rate (Hz).
        order (int): order of the bandpass filter.

    Returns:
        (numpy.ndarray): bandpass filtered data.
    '''
    
    nyq = 0.5 * sample_rate
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    y = filtfilt(b, a, data)
    return y

def buffer(data, duration, data_overlap):
    '''
    Returns segmented data based on the provided input window duration and overlap.

    Args:
        data (pd.DataFrame): dataset. 
        duration (int): window length (number of samples).
        data_overlap (int): number of samples of overlap.

    Returns:
        (numpy.ndarray): segmented data of shape (number_of_segments, duration).
    '''
    # TODO: AVOID tossing out the data
    data = data[:-(data.shape[0] % duration)]
    number_segments = int(math.ceil((len(data) - data_overlap)/(duration - data_overlap)))
    temp_buf = [data[i:i + duration] for i in range(0, len(data), (duration - int(data_overlap)))]
    temp_buf[number_segments-1] = np.pad(temp_buf[number_segments-1],
                            (0, duration - temp_buf[number_segments-1].shape[0]),
                            'constant')
    temp_buf = np.array(temp_buf[:number_segments])
    return temp_buf

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

def parse_eeg(data: pd.DataFrame) -> pd.DataFrame:
    """
    Perform basic parsing on EEG data.

    Args:
        data: The EEG data

    Returns:
        Parsed EEG data
    """
    # offset 1 for Timestep
    if all(data.iloc[0, 1:].values == 0):
        data.at[1, 'Frequency'] = data.loc[0, 'Frequency']
        data.at[1, 'Color Code'] = data.loc[0, 'Color Code']
        data = data[1:]
    datafreqs = data['Frequency'].ffill()
    datafreqs = datafreqs.loc[datafreqs == 0.0]

    data_freqs = data.drop(datafreqs.index)
    
    channel_data = data_freqs.drop(columns=['Time', 'Frequency', 'Color Code'])
    channel_data = channel_data.to_numpy().T
    filtered_data = butter_bandpass_filter(channel_data, 6, 80, 250, 4).T
    df = pd.DataFrame(filtered_data)
    df.columns = [f'CH{i}' for i in range(1, df.shape[1] + 1)]
    df['Time'] = data_freqs['Time']
    df['Frequency'] = data_freqs['Frequency']
    df['Color Code'] = data_freqs['Color Code']
    df.index = np.arange(df.shape[0])
    return df