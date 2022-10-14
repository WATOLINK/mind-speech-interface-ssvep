import socket
import os
import pickle
import sys
import numpy as np
import pandas as pd
from time import time
from collections import Counter
import threading
import glob
from PageFrequencies import page_frequencies
from datetime import datetime

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

    output_size = None  # number of samples needed to fill output array
                        #   the shape of the output array will be 
                        #   (num_channels, sample_rate * window_length)
    fullData = None
    # Buffer Info
    data = None         # data buffer array to be sent to AI
    samples = None      # number of samples currently in buffer

    UIDict = None       # Dict from UI with onset offset mechanism info

    dictionary = None
    
    csvData = None

    def __init__(self, args):
        self.host = args.host
        self.lisPort = args.lisPort
        self.lisPortUI = args.lisPortUI
        self.pubPort = args.pubPort
        self.sample_rate = args.sample_rate

        self.window_length = args.window_length
        self.output_size = args.output_size
        self.num_channels = args.num_channels

        self.data = None
        self.samples = 0
        self.model = load_model(args)

        self.dictionary = {'freq': 0.0, 'page': "Output Menu Page"}
        self.csvData = None

    def open_socket_conn(self):
        self.lisSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lisSocket.connect((self.host, self.lisPort))
        print(f"listening on {self.host}:{self.lisPort}")

        self.lisSocketUI = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lisSocketUI.connect((self.host, self.lisPortUI))
        print(f"listening on {self.host}:{self.lisPortUI}")

        self.pubSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.pubSocket.bind((self.host, self.pubPort))
        self.pubSocket.listen(1)
        print(f"publishing on {self.host}:{self.pubPort}")

    def close_socket_conn(self):
        self.lisSocket.close()
        self.pubSocket.close()
        self.lisSocketUI.close()

    def recieve_packet(self):
        # the size of the input data = num elements * 8 bytes + 500 for leeway
        try:
            sample = self.lisSocket.recv(1000000000)
            sample = pickle.loads(sample)

            pizza_time = sample[:, [0, 1, 2, 3, 4, 5, 6, 7, 17]]
            sample = sample[:, :8]

            # sample = np.hstack((samp,timestamp.T))
            if self.csvData is None:
                self.csvData = pizza_time
            else:
                self.csvData = np.vstack((self.csvData, pizza_time))
            print(self.csvData.shape)
            
        except EOFError:
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
            except EOFError:
                break
            if self.UIDict is None:
                print("no dict received from UI")
        self.close_socket_conn()


    def send_packet(self, sample):
        self.connection.sendall(pickle.dumps(sample))
        print(f'Sent {sample}')
    
    def highest_matching_frequency(self, confidences: np.array, frequencies=None):
        if frequencies is None:
            frequencies = self.model.cca_frequencies
        indices = [self.model.freq2label[freq] for freq in frequencies]
        subset_confidence = confidences[:, indices]
        return self.model.cca_frequencies[indices[np.argmax(subset_confidence, axis=1)[0]]]

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
            if self.UIDict["stimuli"] == "off":
                self.data = None
            else:
                #packet = self.recieve_packet()

                if packet is None:
                    break
                
                if self.data is None:
                    self.data = packet
                else:
                    self.data = np.concatenate((self.data, packet), axis=0)
                if self.data is not None:
                    if self.data.shape[0] == self.sample_rate * self.window_length:
                        sample = np.expand_dims(self.data, axis=0)
                        prepared = self.model.prepare(sample)
                        _, confidence = self.model.predict(prepared)
                        print(f"Prediction made at: {datetime.now()}")
                        frequency = self.highest_matching_frequency(confidences=confidence,
                                                                    frequencies=page_frequencies[self.UIDict['current page']])
                        self.dictionary["freq"] = frequency
                        self.send_packet(self.dictionary)
                        print(f"Prediction sent at: {datetime.now()}")
                        self.data = None
        self.close_socket_conn()

    def generate_csv(self, name="SSVEP-Interface/online_data/eeg.csv"):
        if self.csvData is None:
            print(f"Can't save online session because no data was collected!")
        else:
            os.makedirs("SSVEP-Interface/online_data", exist_ok=True)
            df = pd.DataFrame(data=self.csvData)
            files = glob.glob("SSVEP-Interface/online_data/*.csv")
            if files:
                files.sort()
                name = f"{files[-1][:-5]}{int(files[-1][-5]) + 1}.csv"
            df.to_csv(name, index=False)