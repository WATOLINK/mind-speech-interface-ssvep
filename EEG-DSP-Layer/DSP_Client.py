from sre_constants import SUCCESS
import numpy as np
import pandas as pd
import socket
import pickle
import argparse
from time import time, sleep
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, WindowFunctions
from models.Model import Model
import os

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

    def __init__(self, host='127.0.0.1', port=65432, num_channels=16, input_len=125, output_size = 5,
                model_type: str = 'cca_knn', model_path: os.PathLike = None):
        self.host = host
        self.port = port

        self.input_len = input_len
        self.output_size = output_size
        self.num_channels = num_channels

        self.data = np.empty((output_size*input_len, num_channels))
        self.samples = 0
        self.model = Model(model_path, model_type)

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
            if sample is None:
                print("End of stream")
                return None
            assert type(sample) == np.ndarray,  f"Not a Numpy ND Array {type(sample), sample}"
            assert sample.shape == (self.input_len, self.num_channels), \
                f"Incorrect Shape, Expected: {(self.input_len, self.num_channels)}, Recieved: {sample.shape}"
        return sample

    def listen(self, run_time=None):
        init_time = time()
        time_func = (lambda: time() - init_time < run_time) if run_time else (lambda: True)
        while time_func():
            packet = self.recieve_packet()
            if packet is None:
                print("Streaming stopped suddenly")
                return
            if packet.any():
                start = self.input_len * self.samples 
                end = self.input_len * (self.samples + 1)
                self.data[start:end, :] = packet
                print(f"SUCCESS {self.samples+1}/{self.output_size}")
                del packet
                self.samples = (self.samples + 1) % self.output_size
                if self.samples == 0:
                    self.filter()
                    prediction = self.model.predict(self.data[start:end])
                    print(prediction)
        
    def filter(self):
        num_eeg_channels = 8
        sampling_rate = 256
        mid_freq = 8
        band_width = 8
        for channel in range(num_eeg_channels):
            DataFilter.perform_bandpass(self.data[channel], sampling_rate, mid_freq, band_width, 2, FilterTypes.BUTTERWORTH, 0)

    def generate_csv(self, data, name="fullOBCI"):
        df = pd.DataFrame(data=data, columns=list(range(1,17)))
        print(f'{name}.csv Generated')
        df.to_csv(f'{name}.csv')
        return

def get_args(parser):
    parser.add_argument('--host', type=str, help='ip address', required=False, default='127.0.0.1')
    parser.add_argument('--port', type=int, help='ip port', required=False, default=65432)
    parser.add_argument('--input-len', type=int, help='number of rows in input array', 
        required=False, default=125)
    parser.add_argument('--num-channels', type=int, help='number of columns in input array', 
        required=False, default=16)
    parser.add_argument('--output-size', type=int, help='number of samples needed to fill output array', 
        required=False, default=5)
    parser.add_argument('--model-type', type=str, help='The type of model to use. i.e. CCA with KNN', default='cca_knn')
    parser.add_argument('--model-path', type=str, help='The filepath to the model to use')
    parser.add_argument('--sample-rate', type=int, default=250, help="Sampling rate (hz)")
    parser.add_argument('--window-len', type=int, default=1, help="Window length for data processing")
    parser.add_argument('--shift-len', type=int, default=1, help="Shift length for data processing")
    parser.add_argument('--random-state', type=int, default=42, help="Random State")
    return parser.parse_known_args()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args, _ = get_args(parser)

    listener = EEGSocketListener(args.host, args.port, args.num_channels, args.input_len, args.output_size, args.model_type, args.model_path)
    listener.open_socket_conn()
    listener.listen()