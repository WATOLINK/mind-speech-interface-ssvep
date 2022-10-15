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
from brainflow.board_shim import BrainFlowInputParams
from multiprocessing import Process, Queue, Barrier
import serial.tools.list_ports as p


from DSP_Client import EEGSocketListener
from EEG_socket_publisher import EEGSocketPublisher
from time import time, sleep
from main import mainGUIFunc, create_ui_socket


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


def Streamer(publisher, synch, q, info):
    publisher.open_board_conn(board_id=info[0], board_params=info[1], streamer_params=info[2])
    if publisher.board.get_board_id() == 0 or publisher.board.get_board_id() == 2:
        publisher.col_low_lim = 1
        publisher.col_hi_lim = 9
    synch.wait()
    print(f"Elapsed Time Streamer Process: {time() * 1000} ms")
    try:
        publisher.publish(99999999999)
    finally:
        publisher.close_connections()


def DSP(listener, synch, q):
    synch.wait()
    print("Elapsed Time DSP Process: "+str(round(time() * 1000))+"ms")
    try:
        listener.listen()
    finally:
        listener.close_socket_conn()
        print("generating")
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
    parser.add_argument('--lisPortUI', type=int, help='lis port UI', required=False, default=32111)
    parser.add_argument('--num-channels', type=int, help='number of channels', required=False, default=8)
    parser.add_argument('--input-len', type=int, help='input size', required=False, default=250)
    parser.add_argument('--output-size', type=int, help='output size', required=False, default=1)
    parser.add_argument('--model-type', type=str, help='model type', required=False, default='fbcca')
    parser.add_argument('--model-path', type=str, help='path for saved model', required=False, default=None)
    parser.add_argument('--pubPort', type=int, help='publisher port', required=False, default=55432)
    parser.add_argument('--window-length', type=int, help='window size (s)', required=False, default=4.5)
    parser.add_argument('--shift-length', type=int, help='shift length (s)', required=False, default=1)
    parser.add_argument('--sample-rate', type=int, help='sample rate (hz)', required=False, default=250)
    parser.add_argument('--components', type=int, help='Number of components for CCA', required=False, default=1)
    return parser.parse_known_args()


if __name__ == "__main__":
    sleepTime = 0.25

    parser = argparse.ArgumentParser()
    args, _ = get_args(parser)
    info = Cyton_Board_Config(args)

    publisher = EEGSocketPublisher(args)
    publisher.open_socket_conn()
    client_socket = create_ui_socket()
    listener = EEGSocketListener(args)
    listener.open_socket_conn()

    q = Queue()
    synch = Barrier(2)
    sys_processes = [
        Process(target=mainGUIFunc, args=(client_socket, synch,), name="App"),
        Process(target=Streamer, args=(publisher, synch, q, info), name="Streamer"),
        Process(target=DSP, args=(listener, synch, q,), name="Dsp Client"),
    ]

    for process in sys_processes:
        process.start()
        sleep(sleepTime)
        sleepTime = 0

    for process in sys_processes:
        process.join()
