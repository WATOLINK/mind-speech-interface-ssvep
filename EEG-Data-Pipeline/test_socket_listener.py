import socket
import pickle


class TestSocketListener:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def open_socket_conn(self):
        try:
            self.s.connect(('127.0.0.1', 55432))
        except Exception as e:
            print(f"Couldn't connect to 127.0.0.1:55432, {e}")

    def close_socket_conn(self):
        self.s.close()

    def run(self):
        while True:
            try:
                msg = self.s.recv(1250 * 8 * 8 + 5000000)
                message = pickle.loads(msg)
                print(f"App received: {message}")
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Couldn't listen, raised: {e}")
                self.open_socket_conn()
        self.close_socket_conn()


def run_tsl(synch):
    app = TestSocketListener()
    app.open_socket_conn()
    synch.wait()
    app.run()
