import socket
import os
import pickle
import sys
from turtle import clear
import numpy as np
import pandas as pd
from time import time
import time as t
from brainflow.data_filter import DataFilter, FilterTypes
from collections import Counter
from numpy import savetxt
import threading

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
    listSockerUI = None
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

    UIDict = None       # Dict from UI with onset offset mechanism info

    def __init__(self, args):
        self.host = args.host
        self.lisPort = args.lisPort
        self.lisPortUI = args.lisPortUI
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

        self.lisSocketUI = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lisSocketUI.connect((self.host, self.lisPortUI))

        self.pubSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.pubSocket.bind((self.host, self.pubPort))
        self.pubSocket.listen(1)
        print("listening")

    def close_socket_conn(self):
        self.lisSocket.close()
        self.pubSocket.close()
        self.lisSocketUI.close()

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

    def recieve_packet_UI(self):
        while True:
            try:
                UIDictSerial = self.lisSocketUI.recv(1024)
                self.UIDict = pickle.loads(UIDictSerial)
                print(f"PRINTING UIDict FROM FUNC: {self.UIDict}")
            except EOFError as e:
                print("No dict received from UI")
                print(e)

            if self.UIDict is None:
                print("no dict received from UI")


    def send_packet(self, sample):
        self.connection.sendall(pickle.dumps(sample))
        print(f'Sent {sample}')

    def listen(self, run_time=None):
        self.connection, self.address = self.pubSocket.accept()
        print("Connected by: DSP_Client : "+str(round(time() * 1000))+"ms")
        init_time = time()
        time_func = (lambda: time() - init_time < run_time) if run_time else (lambda: True)

        init_slider_count = 0
        self.data = np.zeros((50,8))

        # Create and start thread
        self.UIDict = {"onOff":1}
        UIthreadRecv = threading.Thread(target=self.recieve_packet_UI)
        UIthreadRecv.start()
        # Initializing it on 1, but it is passed onto the thread, which toggles it every 2 seconds
        
        while time_func:
            packet = self.recieve_packet()
            print(f"Dict: {self.UIDict}")

            if packet is None:
                break

            # first 5 loops - build 250 sample packet from 50 sample packets
            if init_slider_count < 4:
                self.data = np.concatenate((self.data, packet), axis=0)
                print("Building 250 sample packet")
            else:
                self.data = np.concatenate((self.data, packet), axis=0)
                print(f"concatenated size: {np.shape(self.data)}")
                self.data = np.delete(self.data, range(0,50), axis=0)

                print(f"Built 250 sample packet - Packet size: {np.shape(self.data)}")
                sample = self.data[0:250]

                if (self.UIDict["onOff"] == 1):
                    prepared = self.model.prepare(sample)
                    prediction = self.model.predict(prepared)
                    frequencies = self.model.convert_index_to_frequency(prediction)
                    c = Counter(frequencies)
                    print(f"Prediction: {c.most_common(1)[0][0]}")
                    self.send_packet(c.most_common(1)[0][0])
                else:
                    print(f"Prediction not sent")

            init_slider_count += 1

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

