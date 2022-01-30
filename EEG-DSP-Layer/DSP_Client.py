from sre_constants import SUCCESS
import numpy as np
import pandas as pd
import socket
import pickle
import argparse
from time import time, sleep

class EEGSocketListener:
    # Socket Object and Params
    socket = None
    host = ''           # Server hostname or IP
    port = None         # Port used by server

    # Data Format Definitions
    num_channels = None # number of columns in input array 
    input_len = None    # number of rows in input array
    output_size = None  # number of samples needed to fill output array
                        #   the shape of the output array will be 
                        #   (num_channels, input_len*output_size)

    # Buffer Info
    data = None         # data buffer array to be sent to AI
    samples = None      # number of samples currently in buffer

    def __init__(self, host='127.0.0.1', port=65432, num_channels=16, input_len=125, output_size=5):
        self.host = host
        self.port = port

        self.input_len = input_len
        self.output_size = output_size
        self.num_channels = num_channels

        self.data = np.empty((output_size*input_len, num_channels))
        self.samples = 0

    def open_socket_conn(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect( (self.host, self.port) )
    
    def close_socket_conn(self):
        self.socket.close()

    def recieve_packet(self):
        # the size of the input data = num elements * 8 bytes + 500 for leeway
        sample = self.socket.recv(self.input_len * self.num_channels * 8 + 500)
        if sample == None:
            print("Recieved nothing")
        else: # If not null sample is recevied
            sample = pickle.loads(sample)
            assert type(sample) == np.ndarray,  f"Not a Numpy ND Array {type(sample), sample}"
            assert sample.shape == (self.input_len, self.num_channels), \
                f"Incorrect Shape, Expected: {(self.input_len, self.num_channels)}, Recieved: {sample.shape}"
        return sample

    def listen(self, run_time=None):
        init_time = time()
        time_func = (lambda: time() - init_time < run_time) if run_time else (lambda: True)
        while time_func():
            packet = self.recieve_packet()
            if packet.any():
                start = self.input_len * self.samples 
                end = self.input_len * (self.samples + 1)
                self.data[start:end, :] = packet
                print(f"SUCCESS {self.samples+1}/{self.output_size}")
                del packet
                self.samples = (self.samples + 1) % self.output_size
                if self.samples == 0:
                    # TO IMPLEMENT
                    print("OUTPUT BUFFER FILLED, SEND DATA TO AI")
            
    def generate_csv(self, data, name="fullOBCI"):
        df = pd.DataFrame(data=data, columns=list(range(1,17)))
        print(f'{name}.csv Generated')
        df.to_csv(f'{name}.csv')
        return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--host', type=str, help='ip address', required=False, default='127.0.0.1')
    parser.add_argument('--port', type=int, help='ip port', required=False, default=65432)
    parser.add_argument('--input-len', type=int, help='number of rows in input array', 
        required=False, default=125)
    parser.add_argument('--num-channels', type=int, help='number of columns in input array', 
        required=False, default=16)
    parser.add_argument('--output-size', type=int, help='number of samples needed to fill output array', 
        required=False, default=5)
    args = parser.parse_args()

    listener = EEGSocketListener(args.host, args.port, args.num_channels, args.input_len, args.output_size)
    listener.open_socket_conn()
    listener.listen()
