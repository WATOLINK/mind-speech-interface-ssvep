import numpy as np
import pandas as pd
import pickle
import socket

def Client(queue, HOST, PORT):
    # Socket initialization 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    
    # Send signal to server that socket has been connected
    queue.put(True)
    
    ID_pickle = s.recv(1024)
    ID = pickle.loads(ID_pickle)
    print("id received from client: ", ID)
    
    # 
    # TODO: Receive list for column header ("column titles") from Queue, store it in a
    #       variable that is passed into the CSV() function as a parameter
    #

    data = []
    while True:
        sample = s.recv(1000000)

        # If something is recevied over the socket
        if sample: 
            egg = pickle.loads(sample)

            # Data package received
            if egg is not None:
                data.append(egg)

            # Signal for end of data collectionr received
            else:
                break

    csv_export_done = CSV(data, ID)
    queue.put(csv_export_done)


# TODO: Add colour frequency and colour code columns to dataset like in demo.py
def CSV(data, ID):

    # 
    # TODO: Use the column header parameter to add the header to EACH DATAFRAME in the for loop
    #       that converts each element in the "data" list into a dataframe (see the commented out code below)
    #
    print("**********")
    print(type(ID)) 
    if ID == 0 or ID == 2:
        print("Enter")
        header_size = ['CH1', 'CH2', 'CH3', 'CH4', 'CH5', 'CH6', 'CH7', 'CH8']
    elif ID == 8:
        print("Enter")
        header_size = ['CH1', 'CH2', 'CH3', 'CH4', 'CH5', 'CH6', 'CH7', 'CH8']
    elif ID == -1:
        print("Enter")
        header_size = ['CH1', 'CH2', 'CH3', 'CH4', 'CH5', 'CH6', 'CH7', 'CH8', 'CH9', 'CH10']
    
    for i in range(len(data)):
        data[i] = pd.DataFrame(data[i], columns = header_size)

    df = pd.concat(data)
    
    df.index.name = 'Count'
    df.to_csv("TEST_DATA.csv")
    return '-- CSV Exported ' + str(df.shape)