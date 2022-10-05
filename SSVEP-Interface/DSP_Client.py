import socket
import os
import pickle
import sys
import numpy as np
import pandas as pd
from time import time
from collections import Counter
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

    dictionary = None

    def __init__(self, args):
        self.host = args.host
        self.lisPort = args.lisPort
        self.lisPortUI = args.lisPortUI
        self.pubPort = args.pubPort

        self.input_len = args.input_len
        self.window_length = args.window_length
        self.output_size = args.output_size
        self.num_channels = args.num_channels

        self.data = None
        self.samples = 0
        self.model = load_model(args)

        self.dictionary = {'freq': 0.0, 'page': "Output Menu Page"}

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
            # print(e)
            pass

        if sample is None:
            print("COLLECTION COMPLETE")
        return sample

    def recieve_packet_UI(self):
        while True:
            try:
                UIDictSerial = self.lisSocketUI.recv(1024)
                self.UIDict = pickle.loads(UIDictSerial)
                print(self.UIDict)
                print(f"PRINTING UIDict FROM FUNC: {self.UIDict}")
                self.dictionary["page"] = self.UIDict['current page']
            except EOFError as e:
                # print("No dict received from UI")
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

        # Create and start thread
        self.UIDict = {
            'stimuli': 'off',
            'current page': 'Output Menu Page',
            'previous page': '',
            'output mode': ''
        }
        UIthreadRecv = threading.Thread(target=self.recieve_packet_UI)
        UIthreadRecv.start()
        # Initializing it on 1, but it is passed onto the thread, which toggles it every 2 seconds

        while time_func:
            packet = self.recieve_packet()
            if self.UIDict["stimuli"] == "on":
                #packet = self.recieve_packet()

                if packet is None:
                    break
                
                if self.data is None:
                    self.data = packet
                else:
                    self.data = np.concatenate((self.data, packet), axis=0)
                print(np.sum(np.isnan(self.data)), self.data.shape)
                if self.data.shape[0] == self.input_len * self.window_length:
                    sample = np.expand_dims(self.data, axis=0)
                    prepared = self.model.prepare(sample)
                    prediction = self.model.predict(prepared)
                    prediction = [int(pred) for pred in list(prediction)]
                    frequencies = self.model.convert_index_to_frequency(prediction)
                    c = Counter(frequencies)
                    print(f"Prediction: {c.most_common(1)[0][0]}")
                    # If freq prediction does not exist on current UI Page, retry for next highest confidence
                    self.dictionary["freq"] = c.most_common(1)[0][0]
                    self.send_packet(self.dictionary)
                    self.data = None
        self.close_socket_conn()

    def generate_csv(self, name="fullOBCI"):
        df = pd.DataFrame(data=self.data, columns=list(range(1, 9)))
        print(f'{name}.csv Generated')
        df.to_csv(f'{name}.csv')
