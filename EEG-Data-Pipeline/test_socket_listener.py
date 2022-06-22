import socket
from time import sleep
import pickle

    
    
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Instead of bind, connect
s.connect(('127.0.0.1', 55432))

    # TCP socket provides a stream of data to client - receiving data in buffers of 8 bytes from server
    

while True:
            # receiving for port 55432
    msg = s.recv(10000000)
    message = pickle.loads(msg)
    print(message.shape)