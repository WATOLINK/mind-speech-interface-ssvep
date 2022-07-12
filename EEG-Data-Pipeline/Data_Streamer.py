"""
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
"""
import argparse
import pandas as pd
from brainflow.board_shim import BrainFlowInputParams
from multiprocessing import Process, Queue, Barrier
import serial.tools.list_ports as p
import sys

from DSP_Client import EEGSocketListener
from EEG_socket_publisher import EEGSocketPublisher
from test_socket_listener import TestSocketListener, run_tsl

# sys.path.append("SSVEP-Interface")
# from InteractionTestDemo import mainFuncTest


def Cyton_Board_Config(args):
    ports = p.comports()
    print(f'{len(ports)} ports found')
    list_manufacturer = []
    list_ports = []
    for port in ports:
        print(port.manufacturer)
        list_manufacturer.append(port.manufacturer)
        list_ports.append(port.device)

    board_id = 0
    if 'FTDI' in list_manufacturer:
        openbci_index = list_manufacturer.index('FTDI')
        openbci_serial_port = list_ports[openbci_index]
    else:
        board_id = 8 if args.board_id != -1 else -1
        openbci_serial_port = "N/A"

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

    return board_id, params, args.streamer_params


def CSV(data, col):
    start = 0
    end = 50
    for i in range(len(data)):
        # timestamp = np.arange(0, 0.4, 0.008)
        sample_count = [j for j in range(start, end)]
        data[i] = pd.DataFrame(data=data[i], index=sample_count, columns=col)
        start += 50
        end += 50

    df = pd.concat(data, ignore_index=True)
    df.index.name = 'Sample Count'
    df.to_csv('data.csv')


def Streamer(publisher, synch, q, info):
    publisher.open_connections(board_id=info[0], board_params=info[1], streamer_params=info[2])
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
    listener.generate_csv()
    

def get_args(parser):
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
    parser.add_argument('--host', type=str, help='host name', required=False, default='127.0.0.1')
    parser.add_argument('--lisPort', type=int, help='lis port', required=False, default=65432)
    parser.add_argument('--num-channels', type=int, help='number of channels', required=False, default=8)
    parser.add_argument('--input-len', type=int, help='input size', required=False, default=250)
    parser.add_argument('--output-size', type=int, help='output size', required=False, default=5)
    parser.add_argument('--model-type', type=str, help='model type (CCA-KNN)', required=False, default='cca_knn')
    parser.add_argument('--model-path', type=str, help='path for saved model', required=False, default=None)
    parser.add_argument('--pubPort', type=int, help='publisher port', required=False, default=55432)
    parser.add_argument('--window-length', type=int, help='window size (s)', required=False, default=1)
    parser.add_argument('--shift-length', type=int, help='shift length', required=False, default=1)
    parser.add_argument('--sample-rate', type=int, help='sample rate', required=False, default=250)
    parser.add_argument('--components', type=int, help='Number of components for CCA', required=False, default=3)
    return parser.parse_known_args()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args, _ = get_args(parser)
    info = Cyton_Board_Config(args)
    publisher = EEGSocketPublisher(args)
    listener = EEGSocketListener(args)

    q = Queue()
    synch = Barrier(2)
    sys_processes = [Process(target=Streamer, args=(publisher, synch, q, info), name="Streamer"),
                     Process(target=DSP, args=(listener, synch, q,), name="Dsp Client"),
                     Process(target=run_tsl, args=(TestSocketListener(), synch, q))
                     # Process(target=mainFuncTest, name="UI")
                     ]

    for process in sys_processes:
        process.start()

    for process in sys_processes:
        process.join()
