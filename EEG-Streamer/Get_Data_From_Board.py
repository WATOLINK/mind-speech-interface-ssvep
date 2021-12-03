import argparse
import time, sys
import socket
import numpy as np
import pandas as pd
from collections import defaultdict
import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations
from io import StringIO
from io import BytesIO



HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)


def data_stream(board):

    # Data Columns
    # columns = board.get_eeg_names(board_id=2)

    data=''   
    reached_fifty_data = False
    while not reached_fifty_data:
        if board.get_board_data_count() > 50:
        # try if board.get_board_data_count() == 50:
            data = board.get_board_data().transpose()[:, [2,18]]
            reached_fifty_data = True
        else:
            time.sleep(1)

    return data

def ndarray2str(a):
        # Convert the numpy array to string 
        a = a.tobytes()

        return a

def CSV(col):

    columns = ''
    for i in range(len(data)):
        data[i] = pd.DataFrame(data[i], columns=col)
        

    df = pd.concat(data)#, ignore_index=True)
    print(df.shape)
    df.to_csv('data.csv')
    
    for i in params:
        print(i, '\n\n')

    for i in useless:
        print(useless, '\n\n')
    return
    
if __name__ == "__main__":


    BoardShim.enable_dev_board_logger()

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


    # Cyton Board Object
    board = BoardShim(args.board_id, params)

    # Start Acquisition
    board.prepare_session()
    board.start_stream(45000, args.streamer_params)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            t = time.time()
            #while (time.time() - t < 10): 
            out = ndarray2str(data_stream(board))
            conn.sendall(out)
            print('image sent')
            
            resp = conn.recv(1024)
            #if not dataout:
               #print("poop")
                
    board.stop_stream()
    board.release_session()