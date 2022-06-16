import pandas as pd
import numpy as np
import re
from collections import defaultdict

# loading in data
data = pd.read_csv('data\\055_2022_902854.csv')


class Preprocess:

    def __init__(self, data, num_timesteps=1114, num_channels=8, sample_freq=250, type='Frequency'):
        self.type = type  # attribute to process for

        self.data = data
        self.col_names = data.columns
        self.num_trials = data[self.type].value_counts().sum()

        # const
        self.NUM_TIMESTEPS = num_timesteps
        self.NUM_CHANNELS = num_channels
        self.SAMPLING_FREQUENCY = sample_freq

    def _add_trial(self, data):
        data['Trial'] = data[self.type]
        current_label = data.at[0, self.type]

        trial = 0

        # gather similar types into trials
        for i in range(len(data)):

            # upon seeing new label we start counting again
            if data.at[i, self.type] != current_label:
                current_label = data.at[i, self.type]
                trial = 0

            data.at[i, 'Trial'] = trial
            trial += 1

        return data

    def _trim(self, data):
        """

        Args
        ----
        data: Pandas dataframe with 'Count' col
        trim_length: wanted length to trim (int)

        Returns
        -------
        new_df: Pandas dataframe with each trial truncated to trim_length samples

        """

        condition_one = data['Trial'] >= 0
        condition_two = data['Trial'] < self.NUM_TIMESTEPS
        data.where(condition_one & condition_two, inplace=True)
        #data = data.dropna(subset = ['CH1']).reset_index(drop = True)
        data = data.dropna().reset_index(drop=True)

        return data

    def _get_rid_of_nan(self, data):
        """
        makes sure dataset is balanced for training
        """
        condition = data[self.type] != 0  # not interested in data w/ no stimulus?
        data.where(condition, inplace=True)
        data = data.dropna().reset_index(drop=True)

        return data

    def add_t_num(self, data):
        # must get data in a format that groups however many trials for each freq
        # shape in this case [12, 8, 1114, 2] for frequence

        data['Batch'] = None

        labels = defaultdict(int)

        # at every time step (1114) we
        for i in range(0, len(data), self.NUM_TIMESTEPS):
            data.at[i, 'Batch'] = labels[data.at[i, self.type]]
            labels[data.at[i, self.type]] += 1

        data = data.fillna(method="ffill")

        return data

    def get_sorted_df(self, data, condition):

        d = data.copy()

        condition_one = (d['Batch'] == condition)
        d.where(condition_one, inplace=True)
        # print(d[self.type].value_counts())
        d = d.dropna().reset_index(drop=True)

        # sort by Frequency/Color Code
        d = d.sort_values([self.type, 'Trial'])

        return d

    def _get_train_data(self, data):
        col_names = data.columns
        wanted_cols = []

        for i in col_names:
            if re.findall('\ACH', i):
                wanted_cols.append(i)

        training_data = data[wanted_cols]

        return training_data

    def put_together(self, df1, df2):

        df1 = df1.to_numpy()
        df2 = df2.to_numpy()

        together_finally = np.stack((df1, df2), axis=-1)

        # number of timesteps = 1114
        # number of channels = 8
        # number of batches = 2
        t = together_finally.reshape(-1, self.NUM_TIMESTEPS, 8, 2)
        t = np.transpose(t, (0, 2, 1, 3))

        return t

    def process(self):

        # forward fill (frequency or colour code w/ NaN will be filled with previous label)
        new_df = self.data.fillna(method="ffill")

        # gets rid of null cases for now
        new_df = self._get_rid_of_nan(new_df)

        # adds trial col for aid in cleaning
        new_df = self._add_trial(new_df)

        # trims so equal trial lengths
        new_df = self._trim(new_df)

        # adds trial nums (also to help clean)
        new_df = self.add_t_num(new_df)

        # sort the separate batches (2 batches)
        l_data = self.get_sorted_df(new_df, 0)
        r_data = self.get_sorted_df(new_df, 1)

        # gets into nice format ready for train
        new_df1 = self._get_train_data(l_data)
        new_df2 = self._get_train_data(r_data)

        done = self.put_together(new_df1, new_df2)
        return done


if __name__ == "__main__":
    # type can be 'Frequency' or 'Color Code'
    preprocessor = Preprocess(data, type="Frequency")
    d = preprocessor.process()
    print(d.shape)
