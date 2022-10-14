import socket
import os
import pickle
import sys
import numpy as np
import pandas as pd
from time import time
import threading
import glob
from socket_utils import socket_receive
from PageFrequencies import page_frequencies

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

    def receive_packet(self):
        sample = socket_receive(self.lisSocket)
        if sample is None:
            self.close_socket_conn()
            return
        if self.csvData is None:
            self.csvData = sample
        else:
            self.csvData = np.vstack((self.csvData, sample))
        return sample

    def receive_packet_UI(self):
        while True:
            message = socket_receive(self.lisSocketUI)
            if message is None:
                print("no dict received from UI")
                self.close_socket_conn()
                return
            self.UIDict = message
            self.dictionary["page"] = self.UIDict['current page']
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

        # Create and start thread
        self.UIDict = {
            'stimuli': 'off',
            'current page': 'Output Menu Page',
            'previous page': '',
            'output mode': ''
        }
        threading.Thread(target=self.receive_packet_UI).start()
        # Initializing it on 1, but it is passed onto the thread, which toggles it every 2 seconds

        while time_func:
            packet = self.receive_packet()
            if packet is None:
                break
            if self.data is None:
                self.data = packet
            else:
                self.data = np.concatenate((self.data, packet))
            if self.UIDict["stimuli"] == "off" and self.UIDict["on_stimulus_timestamp"]:
                on_stim_time = self.UIDict["on_stimulus_timestamp"]
                off_stim_time = self.UIDict["timestamp"]
                if self.data is not None:
                    subset = self.data[np.nonzero((self.data[:, -1] <= off_stim_time) &
                                                  (self.data[:, -1] >= on_stim_time))]
                    if subset.shape[0] < self.sample_rate * self.window_length:
                        continue
                    diff = subset.shape[0] - self.sample_rate * self.window_length
                    left_diff = diff // 2
                    right_diff = diff - left_diff
                    subset = subset[left_diff: -right_diff]
                    sample = np.expand_dims(subset[:, :-1], axis=0)
                    prepared = self.model.prepare(sample)
                    current_page_frequencies = page_frequencies[self.UIDict['current page']]
                    results, _ = self.model.predict(prepared, frequencies=current_page_frequencies)
                    frequency = self.model.convert_index_to_frequency(results, frequencies=current_page_frequencies)
                    if len(frequency) == 1:
                        frequency = frequency[0]
                    self.dictionary["freq"] = frequency
                    self.send_packet(self.dictionary)
                    self.data = self.data[np.nonzero(self.data[:, -1] > off_stim_time)]
        self.close_socket_conn()

    def generate_csv(self, name="online_data/fullOBCI_1.csv"):
        if self.csvData is None:
            print(f"Can't save online session because no data was collected!")
        else:
            os.makedirs("online_data", exist_ok=True)
            df = pd.DataFrame(data=self.csvData)
            files = glob.glob("online_data/*.csv")
            if files:
                files.sort()
                name = f"{files[-1][:-5]}{int(files[-1][-5]) + 1}.csv"
            df.to_csv(name, index=False)
