import socket
import pickle
import numpy as np

HOST = '127.0.0.1'
PORT = 50007
arr = np.random.rand(50,17)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
conn, addr = s.accept()
print('Connected') 
with conn:
    data_string = pickle.dumps(arr)
    conn.send(b'Fukv')
    print('sent')

    
'''
data = conn.recv(4096)
if not data: break
conn.send(data)
'''
conn.close()