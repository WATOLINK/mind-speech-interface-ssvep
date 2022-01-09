from time import time
import numpy as np
import pandas as pd
import socket, pickle


# Constants that must match constant declaration in sembedded script
HOST = '127.0.0.1'  # Server hostname or IP
PORT = 65432        # Port used by server

# Socket initialization 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect( (HOST, PORT) )

data = []
while True:
    sample = s.recv(100000)
    
    # If sample is recevied
    if sample: 
        egg = pickle.loads(sample)
        if egg is not None:
            data.append(egg)
        else:
            break
        

col = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
for i in range(len(data)):
    data[i] = pd.DataFrame(data[i], columns=col)
df = pd.concat(data)#, ignore_index=True)
print('DONE DONE DONE')
df.to_csv('fullUnicorn.csv')
