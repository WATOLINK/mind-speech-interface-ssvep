import socket
from brainflow.board_shim import BoardShim
import pickle
from time import time
from socket_utils import socket_send


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
        return self.board.get_board_data(self.input_len).T[:, self.col_low_lim:18]

    def send_packet(self, sample):
        socket_send(sending_socket=self.connection, data=sample)
        self.count += 1

    def publish(self, run_time=None):
        self.connection, self.address = self.socket.accept()
        with self.connection:
            print(f'Connected by {self.address}')
            print(f"Connected by: EEG_Socket: {time() * 1000:.0f} ms")
            exp_count = run_time * 2
            init_time = time()
            time_func = (lambda: (self.count < exp_count) and (time() - init_time < run_time + 1)) if run_time else (
                lambda: True)
            while time_func():
                if self.board.get_board_data_count() >= self.input_len:
                    packet = self.retrieve_sample()
                    self.send_packet(packet)
                    print("packet sent")
                    
            self.connection.sendall(pickle.dumps(None))
        self.close_connections()
