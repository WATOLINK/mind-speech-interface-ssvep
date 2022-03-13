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
import argparse
from calendar import EPOCH
import brainflow
import pickle
import socket
import sys
import numpy as np
import pandas as pd
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations
from DSP_Client import Client
from multiprocessing import Process, Queue
from time import time

# Standard loopback interface address (localhost)
HOST = '127.0.0.1' 

# Port to listen on (non-privileged ports are > 1023)
PORT = 65432        

# GTech Unicorn ID is 8
BOARD_ID = 8
DATA_COLLECTION_DURATION = 10    

#Num of Cols:
OPEN_BCI_COL = 8
GTECH_COL = 9
SYNTHETIC_COL = 10

def data_stream(board, queue, conn):
    # Data package counter
    data_package_counter = 0

    global id
    id = board.get_board_data() 
    
    # Open BCI = keep all rows, keep columns 0-8
    # GTech = keep all rows, keep columns 0-9
    if id == 0:
        col_range = OPEN_BCI_COL
    elif id == 8:
        col_range = GTECH_COL
    elif id == -1:
        col_range = SYNTHETIC_COL

    # Clear buffer
    board.get_board_data()

    # Start data collection
    start_time = time()
    while data_package_counter < 10 and time() - start_time < DATA_COLLECTION_DURATION + 1:
        if board.get_board_data_count() >=  250:

            # 
            # TODO: Drop appropriate columns depending on OpenBCI (id = 0), GTech Unicorn (id = 8), 
            #       and virtual board (id = -1). See commented out code directly below
            #
            #       DO NOT use if-else statements inside this while loop. Code inside this while loop 
            #       must be minimized to avoid system latency
            #

            data = board.get_board_data(250).transpose()[:,:col_range]
            sample_out = pickle.dumps(data)
            conn.sendall( sample_out )

            data_package_counter += 1
            print('--', data_package_counter, ' Data Packages Sent ', np.shape(data))

    print('-- Data Collection Complete', time()-start_time)
    conn.sendall(pickle.dumps(None))
    print(board.get_board_id())
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

def Streamer(s, q, id):
    b = Cyton_Board_Config()

    # Wait for signal from DSP that the socket has been connected from the client side
    q.get()

    # 
    # TODO: Send appropriate list for columns header ("column title") depending on OpenBCI (id = 0) 
    #       and GTech Unicorn (id = 8) over the Queue
    #

    # Accept socket connection
    conn, addr = s.accept()

    with conn:
        print('-- Connected by', addr)
        data_stream(b, q, conn)

    print(q.get())
    Cyton_Board_End(b)
    return

def main():

    # 
    # TODO: Use "os" and "sys" libraries to determine which USB dongle (OpenBCI, GTech, or virtual board) 
    #       is connected to the PC's serial port
    #
    global id


    s = Socket_Config()

    # Message queue between server-client processes
    q = Queue()

    # Start concurrent processes
    sys_processes = [ 
                        Process(target=Streamer, args=(s,q,id,)), 
                        Process(target=Client, args=(q,HOST,PORT,id,))    
                    ]

    for process in sys_processes:
        process.start()

    # Wait for both processes to complete executing
    for process in sys_processes:
        process.join()

    Socket_End(s)
    return     

if __name__ == "__main__":
    main()