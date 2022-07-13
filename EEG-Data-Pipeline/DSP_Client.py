import socket
import os
import pickle
import sys
import numpy as np
import pandas as pd
from time import time
from brainflow.data_filter import DataFilter, FilterTypes
from collections import Counter

path = os.getcwd()
head, tail = os.path.split(path)
if tail != 'mind-speech-interface-ssvep':
    path = head
sys.path.append(path)
from eeg_ai_layer.models.Model import load_model


class EEGSocketListener:
    # Socket Object and Params
    lisSocket = None
    pubSocket = None
    host = ''  # Server hostname or IP
    lisPort = None  # Port used by server
    pubPort = None  # Port used to publish to UI

    # Data Format Definitions
    num_channels = None # number of columns in input array 
    input_len = None    # number of rows in input array
    output_size = None  # number of samples needed to fill output array
                        #   the shape of the output array will be 
                        #   (num_channels, input_len * output_size)
    fullData = None
    # Buffer Info
    data = None         # data buffer array to be sent to AI
    samples = None      # number of samples currently in buffer

    def __init__(self, args):
        self.host = args.host
        self.lisPort = args.lisPort
        self.pubPort = args.pubPort

        self.input_len = args.input_len
        self.output_size = args.output_size
        self.num_channels = args.num_channels

        self.data = np.empty((args.output_size * args.input_len, args.num_channels))
        self.samples = 0
        self.model = load_model(args)

    def open_socket_conn(self):
        self.lisSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lisSocket.connect((self.host, self.lisPort))
        self.pubSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.pubSocket.bind((self.host, self.pubPort))
        self.pubSocket.listen(1)
        print("listening")

    def close_socket_conn(self):
        self.lisSocket.close()
        self.pubSocket.close()

    def recieve_packet(self):
        # the size of the input data = num elements * 8 bytes + 500 for leeway
        try:
            sample = self.lisSocket.recv(1000000000)
                # self.input_len * self.num_channels * 8 + 50000)
            sample = pickle.loads(sample)
        except EOFError as e:
            print(e)

        if sample is None:
            print("COLLECTION COMPLETE")
        return sample

    def send_packet(self, sample):
        self.connection.sendall(pickle.dumps(sample))
        print(f'Sent {sample}')

    def listen(self, run_time=None):
        self.connection, self.address = self.pubSocket.accept()
        init_time = time()
        time_func = (lambda: time() - init_time < run_time) if run_time else (lambda: True)
        while time_func:
            packet = self.recieve_packet()
            if packet is None:
                break
            start = self.input_len * self.samples
            end = self.input_len * (self.samples + 1)

            self.data[start:end, :] = packet
            # print(f"SUCCESS {self.samples+1}/{self.output_size} - {np.shape(packet)}")
            # del packet
            # print(f"samples: {self.samples}")
            self.samples = (self.samples + 1) % self.output_size
            if not self.samples:
                # self.filter()
                #sample = self.data[end - self.output_size * self.input_len:end]
                sample = self.data[start:end]
                prepared = self.model.prepare(sample)
                prediction = self.model.predict(prepared)
                frequencies = self.model.convert_index_to_frequency(prediction)
                c = Counter(frequencies)
                print(f"Prediction: {c.most_common(1)[0][0]}")
                self.send_packet((c.most_common(1)[0][0]))

    def filter(self):
        num_eeg_channels = 8
        sampling_rate = 250
        mid_freq = 12
        band_width = 4
        for channel in range(num_eeg_channels):
            DataFilter.perform_bandpass(self.data[channel], sampling_rate, mid_freq, band_width, 2,
                                        FilterTypes.BUTTERWORTH, 0)

    def generate_csv(self, name="fullOBCI"):
        df = pd.DataFrame(data=self.data, columns=list(range(1, 9)))
        print(f'{name}.csv Generated')
        df.to_csv(f'{name}.csv')
        return

