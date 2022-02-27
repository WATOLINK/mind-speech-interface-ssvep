import pandas as pd
from typing import List

def load_data(fp):
    return pd.read_csv(fp)

def split_trials(data: pd.DataFrame) -> List[pd.DataFrame]:
    dropped = data.dropna()
    print(dropped)
    splits = []
    for dropped_index, idx in zip(dropped.index, range(dropped.shape[0] - 1)):
        row = dropped.iloc[idx]
        row_next = dropped.iloc[idx + 1]
        if row.Frequency == 0 and row_next.Frequency == 0:
            splits.append(dropped_index)
    # print(splits)
    res = []
    for split_index in range(1, len(splits)):
        prev_split = splits[split_index - 1]
        curr_split = splits[split_index]
        res.append(data[prev_split:curr_split])
    res.append(data[splits[-1]:])
    for df in res:
        print(df.shape)
    return res

def parse_trial(trial_data: pd.DataFrame):
    # skip first row if all zeros
    if all(trial_data.iloc[0].values() == 0):
        trial_data = trial_data[1:]
    return trial_data

def parse_eeg(data: pd.DataFrame):
    # trials = split_trials(data)
    data['Frequency'] = data['Frequency'].ffill()
    data = data[1:]
    data.index = range(data.shape[0])
    return data



df = load_data('../data/058_2022_007998.csv')
parse_eeg(df)
    
    
    
