import pandas as pd
import numpy as np
import re

# loading in data
#data = pd.read_csv('/Users/mikashaw/code/watolink/trial1.csv')

class Preprocess:
    
    def __init__(self, data, num_timesteps = 1114, num_channels = 8, sample_freq = 250):
        
        self.data = data
        self.col_names = data.columns
        self.num_trials = data['Frequency'].value_counts().sum()
        # this gets the number of trials if 1 trial = testing all 13 classes
        self.num_same_freq = 5 # for curr data format
        
        #const
        self.NUM_TIMESTEPS = num_timesteps
        self.NUM_CHANNELS = num_channels
        self.SAMPLING_FREQUENCY = sample_freq 

    def _get_zero_inds_and_rename(self, data):

        """
        Adds a 'FrequencyTemp' column that differentiates between all 
        the '0' null cases before forward filling as you can't really 
        differentiate betweeen them then.
        """
    
        indices = data.index[data['Frequency'] == 0].tolist()
    
        temp_name = 50
    
        data['FrequencyTemp'] = data['Frequency']
    
        for i in indices:
            data['FrequencyTemp'][i] = temp_name
            temp_name += 1
        
        return data

    def _trim_zero_cases(self, data):
        """
    
        Ensures that the amount of null cases in the dataset is equal to the number of trials
        * Assumes temp start freq = 50
    
        """
    
        START = 50
    
        condition_one = data['FrequencyTemp'] < START + self.num_same_freq
        data.where(condition_one, inplace = True)
        data = data.dropna().reset_index(drop = True)
        return data
        
    def _forward_fill(self, data):
        
        """
        Adds frequency label in column
        """
        filled_data = data.fillna(method = "ffill")
        
        return filled_data
    
    def _add_trial(self, data):
        
        print(data['Frequency'].value_counts())
        data['Trial'] = data['FrequencyTemp']
        current_freq = data['FrequencyTemp'][0]
       
        count_index = 0
        
        for i in range(len(data)):
            
            if data['FrequencyTemp'][i] != current_freq:
                current_freq = data['FrequencyTemp'][i]
                count_index = 0
                
           
            data['Trial'][i] = count_index
            count_index += 1
            #print(count_index)
            
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
        data.where(condition_one & condition_two, inplace = True)
        #data = data.dropna(subset = ['CH1']).reset_index(drop = True)
        data = data.dropna().reset_index(drop = True)

        return data
                
    
    def get_data_arr(self, data):
        
        filled_df = self._forward_fill(data)
        
        #print(filled_df.head())
        return filled_df #for now
    
    def _get_train_data(self, data):
        col_names = data.columns
        wanted_cols = []

        for i in col_names:
            if re.findall('\ACH', i):
                wanted_cols.append(i)

        training_data = data[wanted_cols]

        return training_data
    
    def _get_rid_of_no_freq(self, data):
        
        """
        makes sure dataset is balanced for training
        """
        
        condition = data['Frequency'] != 0
        data.where(condition, inplace = True)
        data = data.dropna().reset_index(drop = True)
        
        return data
        
    #must get data in a format that groups of however many trials for each freq
    # shape in this case [12, 8, 1114, 2]
    
    def add_t_num(self, data):
        data['test'] = None
    
        trial_num = 0
        freqs = {}
    
        for i in data['Frequency'].value_counts().keys():
            freqs[i] = 0
            print(i)
    
        for i in range(0, len(data), 1114):
            data['test'][i] = freqs[data['Frequency'][i]]
            freqs[data['Frequency'][i]] += 1
        
        data = data.fillna(method = "ffill")
    
        return data 
    
    def sort_by_freq(self, data):
    
        # sorts
    
        d = data.sort_values(['Frequency','Trial'])
    
        return d
    
    
    
    def _get_arr_data(self, data):

        """
        Args: 
        -----
        data: pandas dataframe consisting of only channel data

        Returns:
        --------
        new_arr: numpy array of shape [num_frequencies, num_channels, num_timesteps, num_trials]
        """
        
        num_timesteps = self.NUM_TIMESTEPS
        num_channels = self.num_channels
        
        arr_data = data.to_numpy()
        
        num_trials = arr_data.shape[0]//num_timesteps
        # should be 50 for now

        arr_data = arr_data.reshape(num_trials, num_channels, num_timesteps)

        arr_data = np.expand_dims(arr_data, 0)

        arr_data = arr_data.reshape(num_trials, num_channels, num_timesteps, 1) # num trials may change in the future 

        return arr_data 
    
    def get_new_df(self, data, condition):
    
        d = data.copy()
        #print(d.head())
    
        condition_one = d['test'] == condition
        print(condition_one)
        d.where(condition_one, inplace = True)
        d['Frequency'].value_counts()
        #data = data.dropna(subset = ['CH1']).reset_index(drop = True)
        d = d.dropna().reset_index(drop = True)

        return d

    def _put_together(self, all_data):

        for df in all_data:
            df = df.to_numpy() 

        together_finally = np.stack(all_data, axis = -1)
        t = together_finally.reshape(13, 1114, 8, 5)
        t = np.transpose(t, (0,2,1,3))
    
        return t

    
    def put_together(self, df1, df2):
    
        df1 = df1.to_numpy()
        df2 = df2.to_numpy()

    
        together_finally = np.stack((df1,df2), axis = -1)
        t = together_finally.reshape(13, 1114, 8, 2)
        t = np.transpose(t, (0,2,1,3))
    
        return t
    

    def main(self):

        #load data
        #print(self.num_trials)
        #print(self.data['Frequency'].value_counts())
        
        # adds col for organizing null cases
        new_df = self._get_zero_inds_and_rename(self.data)

        #forward fill
        new_df = self.get_data_arr(new_df)

        # ensures same amount of null cases as other freqs
        new_df = self._trim_zero_cases(new_df)
      
        #gets rid of null cases for now
        #new_df = self._get_rid_of_no_freq(new_df)
        
        #print(new_df['Frequency'].value_counts())
        
        #adds trial col for aid in cleaning
        new_df = self._add_trial(new_df)
        
        #trims so equal trial lengths
        new_df = self._trim(new_df)
        
        #adds trial nums (also to help clean)
        new_df = self.add_t_num(new_df)
        print(new_df['test'].value_counts())
        print("=======DATA========")
        print(new_df['Frequency'].value_counts())
        


        #in this case
        # iterate through num needed 
        all_data = []
        for i in range(5):
            temp_data = self.get_new_df(new_df, i)
            temp_data = self.sort_by_freq(temp_data)
            all_data.append(self._get_train_data(temp_data))
        #l_data = self.get_new_df(new_df, 0)
        #r_data = self.get_new_df(new_df,1)
        
        #sort both by frequency 
        #l_data = self.sort_by_freq(l_data)
        #r_data = self.sort_by_freq(r_data)
        
        #gets into nice format ready for train
        #new_df1 = self._get_train_data(l_data)
        #new_df2 = self._get_train_data(r_data)
        
        done = self._put_together(all_data)
        
        
        return done
        
if __name__ == "__main__":
    data = pd.read_csv('./emily_trial1.csv')
    preprocessor = Preprocess(data)
    d = preprocessor.main() 
    print(d.shape)

