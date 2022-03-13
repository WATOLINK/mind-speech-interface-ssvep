import argparse, socket, pickle, sys
import numpy as np
import pandas as pd
from collections import defaultdict
import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations
from time import time

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)


def data_stream(board, conn, num_samples=250):

    data=''
    all_data = []
    columns = board.get_eeg_names(board_id=2)[1:9]

    count = 0
    ti = time()
    while time() - ti < 9999:
        
        if board.get_board_data_count() >=  num_samples:

            data = board.get_board_data(num_samples).transpose()[:,1:9] 
            sample_out = pickle.dumps(data)
            conn.sendall(sample_out)
            print(data.shape)
            count += 1
            print('Data sent', count)
            # time.sleep(num_samples/sampling rate) this could be done to be more efficient
    
    conn.sendall(pickle.dumps(None))

    # Call CSV
    # Thread(CSV(all_data, columns))

    return

def Cyton_Board_Config():
    
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
    parser.add_argument('--sample-rate', type=int, help='sample rate', required=False, default=250)
    parser.add_argument('--num-channels', type=int, help='Number of channels', required=False, default=8)
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
    b.stop_stream()
    b.release_session()
    return

def Socket_End(sock):
    sock.close()
    return

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

    b = Cyton_Board_Config()
    s = Socket_Config()

    conn, addr = s.accept()
    
    with conn:
        print('Connected by', addr)
        data_stream(b, conn)
        
    print('DONE DONE DONE')

    Socket_End(s)
    Cyton_Board_End(b)     
