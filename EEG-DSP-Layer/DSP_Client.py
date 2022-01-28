import numpy as np
import pandas as pd
import socket
import pickle
import argparse

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

        self.data = np.empty((num_channels, output_size*input_len))
        self.samples = 0

    def open_socket_conn(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect( (self.host, self.port) )

    def recieve_packet(self):
        # the size of the input data = num elements * 8 bytes + 500 for leeway
        sample = self.socket.recv(self.input_len * self.num_channels * 8 + 500)
        # If sample is recevied
        if sample: 
            sample = pickle.loads(sample)
            assert type(sample) == np.ndarray,  "Not a Numpy ND Array"
            assert sample.shape == (self.input_len, self.num_channels), "Incorrect Shape"
            return sample
        else:
            print("Recieved nothing")
            return None

    def listen(self):
        while True:
            egg = self.recieve_packet()
            if egg:
                start = self.input_len * self.samples 
                end = self.input_len * (self.samples + 1)
                self.data[:, start:end] = egg
                samples = (samples + 1) % self.output_size
            
    def generate_csv(self, name="fullOBCI"):
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
        quired=False, default=5)
    args = parser.parse_args()

    listener = EEGSocketListener(args.host, args.port, args.input_len, args.num_channels, args.output_size)
