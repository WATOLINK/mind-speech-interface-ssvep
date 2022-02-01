import numpy as np
import pandas as pd
import pickle
import socket

def Client(queue, HOST, PORT, ID):
    # Socket initialization 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    # Send signal to server that socket has been connected
    queue.put(True)
    
    data = []
    while True:
        sample = s.recv(100000)

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

    if ID == 0:
        pass
    elif ID == 8:
        pass
    # Virtual board
    else:
        col = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]

    #header = ['Time']
    #for i in range(1, 17):
    #    header.append('CH{}'.format(i))

    for i in range(len(data)):
        data[i] = pd.DataFrame(data[i])#, columns=header)

    df = pd.concat(data)
    df.index.name = 'Count'
    df.to_csv("TEST_DATA.csv")
    return '-- CSV Exported ' + str(df.shape)

    
