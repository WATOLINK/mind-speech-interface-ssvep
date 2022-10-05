from multiprocessing import synchronize
from multiprocessing.connection import wait
import socket
import pickle
import time as time

# def testOnsetOffset():
if __name__ == "__main__":

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 32111))
    s.listen(1)
    # synch.wait()

    offDict = {'onOff' : 0}
    onDict = {'onOff' : 1}

    while True:

        # client socket object and where its coming from (IP)
        print("LOOKING FOR CONNECTIONS")
        clientsocket, address = s.accept()
        print(f"CONNECTION FROM DSP_CLIENT HAS BEEN ESTABLISHED")

        while True:
            # Send 1
            serialOffDict = pickle.dumps(offDict)
            clientsocket.send(serialOffDict)
            print("OffDict sent")
            time.sleep(2)

            # Send 0
            serialOnDict = pickle.dumps(onDict)
            clientsocket.send(serialOnDict)
            print("OnDict sent")
            time.sleep(2)
