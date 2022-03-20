'''
    * Streamer script that interfaces with both OpenBCI and GTech Unicorn hardware
    * Uses multiprocessing for simultaneous server-client model with the DSP post-processing script 
    * Refer to https://brainflow.readthedocs.io/en/stable/UserAPI.html#python-api-reference for useful functions
    
    * Terminal call:
        /EEG-Streamer/
            python Embedded_Server.py --board-id=<BOARD_ID> --serial-port=<SERIAL_PORT>
    * Helpful information:
        OpenBCI Sample Rate:       125Hz (i.e. 125 rows of data per second)
        GTech Unicorn Sample Rate: 250Hz (i.e. 250 rows of data per second)
        OpenBCI ID:         0
        GTech Unicorn ID:   8
        Virutal Board ID:  -1
        Process 1 = Streamer() function in Embedded_Server.py
        Process 2 = Client() function in DSP_Client.py
        TEST_DATA.csv in /EEG-Streamer/ directory is the output CSV from DSP_Client.py
'''
import argparse, socket, pickle, sys
import numpy as np
import pandas as pd
import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations
from time import time

class EEGSocketPublisher:
    # Socket Object and Params
    socket = None
    host = ''           # Standard loopback interface address (localhost)
    port = None         # Port to listen on (non-privileged ports are > 1023)

    board = None
    count = 0

    # Data Format Definitions
    num_channels = None # number of columns in input array 
    input_len = None    # number of rows in input array

    def __init__(self, host='127.0.0.1', port=65432, num_channels=16, input_len=125):
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
        sample = self.board.get_board_data(self.input_len).T[:,1:17]
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
    # use docs to check which parameters are required for specific board, e.g. for Cyton - set serial port
    parser.add_argument('--timeout', type=int, help='timeout for device discovery or connection', required=False, default=0)
    parser.add_argument('--ip-port', type=int, help='ip port', required=False, default=0)
    parser.add_argument('--ip-protocol', type=int, help='ip protocol, check IpProtocolType enum', required=False, default=0)
    parser.add_argument('--ip-address', type=str, help='ip address', required=False, default='')
    parser.add_argument('--serial-port', type=str, help='serial port', required=False, default='')
    parser.add_argument('--mac-address', type=str, help='mac address', required=False, default='')
    parser.add_argument('--other-info', type=str, help='other info', required=False, default='')
    parser.add_argument('--streamer-params', type=str, help='streamer params', required=False, default='')
    parser.add_argument('--serial-number', type=str, help='serial number', required=False, default='')
    parser.add_argument('--board-id', type=int, help='board id, check docs to get a list of supported boards', required=True)
    parser.add_argument('--file', type=str, help='file', required=False, default='')
    args = parser.parse_args()

    params = BrainFlowInputParams()
    params.ip_port = args.ip_port
    params.serial_port = args.serial_port
    params.mac_address = args.mac_address
    params.other_info = args.other_info
    params.serial_number = args.serial_number
    params.ip_address = args.ip_address
    params.ip_protocol = args.ip_protocol
    params.timeout = args.timeout
    params.file = args.file

    return args.board_id, params, args.streamer_params

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
    
if __name__ == "__main__":

    board_id, params, streamer_params = Cyton_Board_Config()
    publisher = EEGSocketPublisher()

    publisher.open_connections(board_id, params, streamer_params)
    publisher.publish(10)
    publisher.close_connections()
