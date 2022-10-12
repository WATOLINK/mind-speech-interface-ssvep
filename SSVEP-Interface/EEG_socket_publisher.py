import socket
from brainflow.board_shim import BoardShim
import numpy as np
import pickle
from time import time


class EEGSocketPublisher:
    # Socket Object and Params
    socket = None
    host = ''  # Standard loopback interface address (localhost)
    port = None  # Port to listen on (non-privileged ports are > 1023)

    board = None
    count = 0

    col_low_lim = 0
    col_hi_lim = 8

    # Data Format Definitions
    num_channels = None  # number of columns in input array
    input_len = None  # number of rows in input array

    def __init__(self, args):
        self.host = args.host
        self.port = args.lisPort

        self.input_len = args.input_len
        self.num_channels = args.num_channels

    def open_socket_conn(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen()

    def close_socket_conn(self):
        self.socket.close()

    def open_board_conn(self, board_id, board_params, streamer_params):
        BoardShim.enable_dev_board_logger()
        self.board = BoardShim(board_id, board_params)
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
        # self.col_hi_lim = r.randint(2,8)
        sample = self.board.get_board_data(self.input_len).T[:, self.col_low_lim:self.col_hi_lim]
        assert type(sample) == np.ndarray, f"Not a Numpy ND Array {type(sample), sample}"
        assert sample.shape == (self.input_len, self.num_channels), \
            f"Incorrect Shape, Expected: {(self.input_len, self.num_channels)}, Recieved: {sample.shape}"
        return sample

    def send_packet(self, sample):
        self.connection.sendall(pickle.dumps(sample))
        self.count += 1

    def publish(self, run_time=None):
        self.connection, self.address = self.socket.accept()
        with self.connection:
            print('Connected by', self.address)
            print("Connected by: EEG_Socket : "+str(round(time() * 1000))+"ms")
            exp_count = run_time * 2
            init_time = time()
            time_func = (lambda: (self.count < exp_count) and (time() - init_time < run_time + 1)) if run_time else (
                lambda: True)
            init_time = round(init_time * 1000)
            while time_func():
                if self.board.get_board_data_count() >= self.input_len:
                    packet = self.retrieve_sample()
                    self.send_packet(packet)
                    
            self.connection.sendall(pickle.dumps(None))
            
