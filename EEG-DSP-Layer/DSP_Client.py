from sre_constants import SUCCESS
import socket
import os
import pickle
import sys
import numpy as np
import pandas as pd
from time import time
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, WindowFunctions

path = os.getcwd()
if path.split('\\')[-1] != 'mind-speech-interface-ssvep':
    path = os.path.join(*path.split('\\')[:-1])
sys.path.append( path + '\EEG-AI-Layer' )
#from models.Model import Model

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

    def __init__(self, host='127.0.0.1', port=65432, num_channels=8, input_len=125, output_size=5,
                model_type: str = 'cca_knn', model_path: os.PathLike = None):
        self.host = host
        self.port = port

        self.input_len = input_len
        self.output_size = output_size
        self.num_channels = num_channels

        self.data = np.empty((output_size*input_len, num_channels))
        self.samples = 0
        #self.model = Model(model_path, model_type)
        
        self.samplling_rate_hz = 250
        self.window_len = 1
        self.shift_len = 1
        self.random_state = 42

    def open_socket_conn(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect( (self.host, self.port) )
    
    def close_socket_conn(self):
        self.socket.close()

    def recieve_packet(self):
        # the size of the input data = num elements * 8 bytes + 500 for leeway
        sample = self.socket.recv(self.input_len * self.num_channels * 8 + 500)
        sample = pickle.loads(sample)
        if sample is None:
            print("COLLECTION COMPLETE")
        else: # If not null sample is recevied
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
                break
            start = self.input_len * self.samples 
            end = self.input_len * (self.samples + 1)
            self.data[start:end, :] = packet
            print(f"SUCCESS {self.samples+1}/{self.output_size} - {np.shape(self.data)}")
            del packet
            self.samples = (self.samples + 1) % self.output_size
            if self.samples == 0:
                #self.filter()
                #prediction = self.model.predict(self.data[start:end])
                #print(prediction)
                print('TODO: MODEL PREDICTION')
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