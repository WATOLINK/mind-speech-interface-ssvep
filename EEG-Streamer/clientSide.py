import numpy as np
from io import StringIO
from io import BytesIO
import scipy.io as sio
from sklearn.cross_decomposition import CCA
import socket, pickle


HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    sample = s.recv(100000)

    if not sample: break
    data = pickle.loads(sample)
    
print('Data received\n')
print(data, '\n\n')
print(data.shape)