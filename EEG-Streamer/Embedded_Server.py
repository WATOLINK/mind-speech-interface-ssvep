'''
    * Streamer script that interfaces with both OpenBCI and GTech Unicorn hardware
    * Uses multiprocessing for simultaneous server-client model with the DSP post-processing script 
    * Refer to https://brainflow.readthedocs.io/en/stable/UserAPI.html#python-api-reference for useful functions
    
    * Terminal call:
        /EEG-Streamer/
            python Embedded_Server.py --board-id=<BOARD_ID> --serial-port=<SERIAL_PORT>


    OpenBCI Sample Rate:       125Hz
    GTech Unicorn Sample Rate: 250Hz

    OpenBCI ID:         0
    GTech Unicorn ID:   8
    Virutal Board ID:  -1

'''
import argparse
from tracemalloc import start
import brainflow
import pickle
import socket
import sys
import numpy as np
import pandas as pd
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations
from DSP_Client import Client
from collections import defaultdict
from multiprocessing import Process, Queue
from time import time, sleep

# Standard loopback interface address (localhost)
HOST = '127.0.0.1' 

# Port to listen on (non-privileged ports are > 1023)
PORT = 65432        

# GTech Unicorn ID is 8
BOARD_ID = 8
DATA_COLLECTION_DURATION = 10       

def data_stream(board, queue, conn):
    # Data package counter
    data_package_counter = 0

    # Clear buffer
    board.get_board_data()
    
    # Start data collection
    start_time = time()
    while data_package_counter < 10 and time() - start_time < DATA_COLLECTION_DURATION + 1:
        if board.get_board_data_count() >=  250:

            # -- col[17] == Unix time           
            data = board.get_board_data(250).transpose()#[:,:8]
            sample_out = pickle.dumps(data)
            conn.sendall( sample_out )

            data_package_counter += 1
            print('--', data_package_counter, ' Data Packages Sent ', np.shape(data))

    print('-- Data Collection Complete', time()-start_time)
    conn.sendall(pickle.dumps(None))
    return

def Cyton_Board_Config():
    BoardShim.enable_dev_board_logger()

    # Terminal parameters
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
    
    # Cyton Board Object
    board = BoardShim(args.board_id, params)

    # Start Acquisition
    board.prepare_session()
    board.start_stream(45000, args.streamer_params)
    return board

def Socket_Config():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen()
    return sock

def Cyton_Board_End(board):
    board.stop_stream()
    board.release_session()
    return

def Socket_End(sock):
    sock.close()
    return

def Streamer(s, q):
    b = Cyton_Board_Config()
    q.get()
    conn, addr = s.accept()

    with conn:
        print('-- Connected by', addr)
        data_stream(b, q, conn)

    print(q.get())
    Cyton_Board_End(b)
    return

def main():
    s = Socket_Config()
    q = Queue()

    sys_processes = [ Process(target=Streamer, args=(s,q,)), Process(target=Client, args=(q,HOST,PORT,BOARD_ID,)) ]
    for process in sys_processes:
        process.start()

    for process in sys_processes:
        process.join()

    Socket_End(s)
    return     

if __name__ == "__main__":
    main()