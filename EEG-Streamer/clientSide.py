import numpy as np
from io import StringIO
from io import BytesIO
import scipy.io as sio
from sklearn.cross_decomposition import CCA
import socket


HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

def str2ndarray(a):
        # Specify your data type, mine is numpy float64 type, so I am specifying it as np.float64
        a = np.frombuffer(a)

        return a

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello, world')
    #ultimate_buffer=''
    while True:
        receiving_buffer = s.recv(1024)
        print('test')
        #receiving_buffer = receiving_buffer.decode()
        if not receiving_buffer: break
        #ultimate_buffer += receiving_buffer
        image = str2ndarray(receiving_buffer)

    print('\nframe received')
    print(image)