'''
    * Streamer script that interfaces with both OpenBCI and GTech Unicorn hardware
    * Uses multiprocessing for simultaneous server-client model with the DSP post-processing script 
    * Refer to https://brainflow.readthedocs.io/en/stable/UserAPI.html#python-api-reference for useful functions
    
    * Terminal call:
        /EEG-Streamer/
            python Embedded_Server.py --board-id=<BOARD_ID> --serial-port=<SERIAL_PORT>
    * Helpful information:
        OpenBCI Sample Rate:       250Hz (i.e. 250 rows of data per second)
        GTech Unicorn Sample Rate: 250Hz (i.e. 250 rows of data per second)
        OpenBCI ID:         0
        GTech Unicorn ID:   8
        Virutal Board ID:  -1
        Process 1 = Streamer() function in Embedded_Server.py
        Process 2 = Client() function in DSP_Client.py
        TEST_DATA.csv in /EEG-Streamer/ directory is the output CSV from DSP_Client.py
'''
import argparse
from calendar import EPOCH
import brainflow
import os
import pickle
import socket
import sys
import numpy as np
import pandas as pd
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations
from multiprocessing import Process, Queue, Barrier
from time import time
import serial.tools.list_ports as p

sys.path.append( '../EEG-DSP-Layer' )
import sys
from PyQt5.QtCore import center, Qt
from PyQt5.QtGui import QFont

from PyQt5.QtWidgets import QApplication, QStackedWidget
from PyQt5.QtWidgets import QMainWindow
from DSP_Client import EEGSocketListener

sys.path.append(os.path.abspath("C:/Users/adali/Desktop/mind-speech-interface-ssvep/SSVEP-Interface"))
from InteractionTestDemo import mainFuncTest

class EEGSocketPublisher:
    # Socket Object and Params
    socket = None
    host = ''           # Standard loopback interface address (localhost)
    port = None         # Port to listen on (non-privileged ports are > 1023)

    board = None
    count = 0

    col_low_lim = 0
    col_hi_lim = 8

    # Data Format Definitions
    num_channels = None # number of columns in input array 
    input_len = None    # number of rows in input array

    def __init__(self, host='127.0.0.1', port=65432, num_channels=8, input_len=250):
        self.host = host
        self.port = port

        self.input_len = input_len
        self.num_channels = num_channels

    def open_socket_conn(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind( (self.host, self.port) )
        self.socket.listen()
    
    def close_socket_conn(self):
        self.socket.close()
    
    def open_board_conn(self, board_id, params, streamer_params):
        BoardShim.enable_dev_board_logger()
        self.board = BoardShim(board_id, params)
        # Start Acquisition
        self.board.prepare_session()
        self.board.start_stream(45000, streamer_params)

    def close_board_conn(self):
        self.board.stop_stream()
        self.board.release_session()

    def open_connections(self, board_id, board_params, streamer_params):
        self.open_socket_conn()
        self.open_board_conn(board_id, board_params, streamer_params)
    
    def close_connections(self):
        self.close_socket_conn()
        self.close_board_conn()

    def retrieve_sample(self):
        sample = self.board.get_board_data(self.input_len).T[:,self.col_low_lim:self.col_hi_lim]
        assert type(sample) == np.ndarray,  f"Not a Numpy ND Array {type(sample), sample}"
        assert sample.shape == (self.input_len, self.num_channels), \
            f"Incorrect Shape, Expected: {(self.input_len, self.num_channels)}, Recieved: {sample.shape}"
        return sample
    
    def send_packet(self, sample):
        self.connection.sendall(pickle.dumps(sample))
        self.count += 1
        print('Data sent,', self.count)
        print(sample.shape)

    def publish(self, run_time=None):
        self.connection, self.address = self.socket.accept()
        with self.connection:
            print('Connected by', self.address)
            exp_count = run_time * 2 
            init_time = time()
            time_func = (lambda: (self.count < exp_count) and (time() - init_time < run_time + 1) ) if run_time else (lambda: True)
            while time_func():
                if self.board.get_board_data_count() >=  self.input_len:
                    packet = self.retrieve_sample()
                    self.send_packet(packet)

            self.connection.sendall(pickle.dumps(None))

def Cyton_Board_Config():
    parser = argparse.ArgumentParser()

    parser.add_argument('--timeout', type=int, help='timeout for device discovery or connection', required=False, default=0)
    parser.add_argument('--ip-port', type=int, help='ip port', required=False, default=0)
    parser.add_argument('--ip-protocol', type=int, help='ip protocol, check IpProtocolType enum', required=False, default=0)
    parser.add_argument('--ip-address', type=str, help='ip address', required=False, default='')
    parser.add_argument('--serial-port', type=str, help='serial port', required=False, default='')
    parser.add_argument('--mac-address', type=str, help='mac address', required=False, default='')
    parser.add_argument('--other-info', type=str, help='other info', required=False, default='')
    parser.add_argument('--streamer-params', type=str, help='streamer params', required=False, default='')
    parser.add_argument('--serial-number', type=str, help='serial number', required=False, default='')
    parser.add_argument('--board-id', type=int, help='board id, check docs to get a list of supported boards', required=False)
    parser.add_argument('--file', type=str, help='file', required=False, default='')
    args = parser.parse_args()

    ports = p.comports()
    print(len(ports), 'ports found')
    list_manufacturer = []
    list_ports = []
    for port in ports:
            print(port.manufacturer)
            list_manufacturer.append(port.manufacturer)
            list_ports.append(port.device)
        
    argument = str(sys.argv)
    if list_manufacturer.__contains__('FTDI'):
        id = 0
        openbci_index = list_manufacturer.index('FTDI')
        openbci_serial_port = list_ports[openbci_index]
    else:
        print("Arguments: " , argument)
        if (argument.__contains__('--board-id=-1')):
            id = -1
        else:
            id = 8
        openbci_serial_port = "N/A"
    print(id)

    params = BrainFlowInputParams()
    params.ip_port = args.ip_port
    params.serial_port = openbci_serial_port
    params.mac_address = args.mac_address
    params.other_info = args.other_info
    params.serial_number = args.serial_number
    params.ip_address = args.ip_address
    params.ip_protocol = args.ip_protocol
    params.timeout = args.timeout
    params.file = args.file

    return (id, params, args.streamer_params)

def CSV(data, col):
    start = 0
    end   = 50
    for i in range(len(data)):
        #timestamp = np.arange(0, 0.4, 0.008)
        sample_count = [j for j in range(start,end)]
        data[i] = pd.DataFrame(data=data[i], index=sample_count, columns=col)
        start +=50
        end   +=50

    df = pd.concat(data, ignore_index=True)
    df.index.name = 'Sample Count'
    print(df.shape)
    df.to_csv('data.csv')
    return
    
def Streamer(publisher, synch, q, info):
    publisher.open_connections(info[0], info[1], info[2])
    if publisher.board.get_board_id() == 0 or publisher.board.get_board_id() == 2:
        publisher.col_low_lim = 1
        publisher.col_hi_lim = 9
    synch.wait()
    publisher.publish(10)
    if q.get() is None:
        publisher.close_connections()
        q.put(None)

def DSP(listener, synch, q):
    listener.open_socket_conn()
    
    synch.wait()
    listener.listen()
    q.put(None)
    if q.get() is None:
        listener.close_socket_conn()



if __name__ == "__main__":
    info = Cyton_Board_Config()
    publisher = EEGSocketPublisher()
    listener = EEGSocketListener()
    


    q = Queue()
    synch = Barrier(2)
    sys_processes = [ Process(target=Streamer, args=(publisher, synch, q, info)), 
                      Process(target=DSP, args=(listener, synch, q,)),
                      Process(target=mainFuncTest) ]

    for process in sys_processes:
        process.start()

    for process in sys_processes:
        process.join()
    
    
