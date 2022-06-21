import socket
from time import sleep
import pickle
class testSock:
    s = None
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Instead of bind, connect
        self.s.connect(('127.0.0.1', 55432))

    # TCP socket provides a stream of data to client - receiving data in buffers of 8 bytes from server
    """ full_msg = ''
    while True:
        msg = s.recv(8)
        if len(msg) <= 0:
            break
        full_msg += msg.decode("utf-8") """
    def contSock(self):
        while True:
            # receiving for port 55432
            msg = self.s.recv(10000000)
            message = pickle.loads(msg)
            print(message.shape)