import socket, pickle
import numpy as np

HOST = '127.0.0.1'
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
while True:
    data = s.recv(100000)
    if not data: break
    data_arr = pickle.loads(data)
    print(data_arr)
    print(type(data_arr))
    data = data.decode('utf-8')
    print('\n\n', data)
s.close()
print (data_arr.shape)