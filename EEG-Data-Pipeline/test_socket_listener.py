import socket
import pickle

def run_tsl(app, synch, q):
    app.open_socket_conn()
    synch.wait()
    app.run()
    # if q.get() is None:
    #     app.close_socket_conn()

class TestSocketListener:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def open_socket_conn(self):
        try:
            self.s.connect(('127.0.0.1', 55432))
        except:
            pass

    def close_socket_conn(self):
        self.s.close()

    def run(self):
        while True:
            try:
                msg = self.s.recv(1250 * 8 * 8 + 5000000)
                message = pickle.loads(msg)
                print(message)
            except:
                self.open_socket_conn()
