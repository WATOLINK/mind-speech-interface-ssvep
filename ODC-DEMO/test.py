import pandas as pd
import numpy as np

color_code_order = [1, 2, 3, 4, 5]
color_freq_order = [10,20,30,40,50]



def colour_freq_process(df):
    index_epoch_list = []
    for i in range( df['Count'].size ):
        if df['Count'][i] == 0.0:
            index_epoch_list.append( i )
    print(index_epoch_list)

    print('\n\n\n', len(index_epoch_list))
    
    '''
    for i in range(len(color_code_order)):
        df.loc[index_epoch_list[i], 'Color Code'] = color_code_order[i]
        df.loc[index_epoch_list[i], 'Frequency'] = color_freq_order[i]
    print(df.head())
    df.to_csv('test.csv')
    
def timestamp_process( data, timestamp ):
    for i in range(np.shape( timestamp )[0]):
        data[i] = np.c_[ timestamp[i] , data[i]  ]
    
if __name__ == '__main__':
    df = pd.read_csv("dummy_test_data.csv")
    colour_freq_process(df)
    '''
    data = []
    timestamp = []
    for i in range(4):
        data.append(np.random.rand(3,3))
        timestamp.append(np.random.rand(3, 1))

    timestamp_process(data, timestamp)
    '''
    
