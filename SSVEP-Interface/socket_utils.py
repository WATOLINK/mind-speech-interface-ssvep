"""Socket Utils"""
import socket
import pickle
import sys
from typing import Any


def socket_receive(receiving_socket: socket.socket, sep=b":") -> bool:
    """
    Receive data from the receiving socket.

    Args:
        receiving_socket: The socket that will receive data. The socket must be connected.
        sep: The separator used to separate the length data from the message data

    Returns:
        The received data
    """
    if not isinstance(sep, bytes):
        sep = sep.encode()
    total_len = 0
    total_data = []
    size = sys.maxsize
    size_data = b""
    recv_size = 8192
    while total_len < size:
        try:
            sock_data = receiving_socket.recv(recv_size)
        except EOFError:
            return
        if total_data:
            total_data.append(sock_data)
            total_len += len(sock_data)
        else:
            if sep not in sock_data:
                # Still receiving the size of the message
                size_data += sock_data
            else:
                sep_index = sock_data.index(sep)
                size = pickle.loads(size_data + sock_data[:sep_index])
                message = sock_data[sep_index + 1:]
                total_len += len(message)
                total_data.append(message)
    return pickle.loads(b''.join(total_data))


def socket_send(sending_socket: socket.socket, data: Any, sep=b":"):
    """
    Receive data from the receiving socket.

    Args:
        sending_socket: The socket to send data from
        data: The data to be sent
        sep: The separator used to separate the length data from the message data
    """
    if not isinstance(sep, bytes):
        sep = sep.encode()
    pickled_sample = pickle.dumps(data)
    length = pickle.dumps(len(pickled_sample))
    message = length + sep + pickled_sample
    # sendall continues to send data until there's nothing left in the buffer
    # this implies that data can be (and is often) sent piece-meal
    # but also implies that data has to be received piece-meal
    sending_socket.sendall(message)
