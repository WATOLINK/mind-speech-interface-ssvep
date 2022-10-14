import sys
import asyncio
import websockets
from PyQt5.QtCore import center, Qt

from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QMainWindow, QStackedWidget, QLabel
from UI.status import getStatus

from UI.MainWidget.mainWidget import MainContainer
from UI.styles import windowStyle

from UI.Components.button_container import ButtonContainer#, buttonClickNoise
from UI.status import printStatus, setStimuliStatus
from UI.UI_DEFS import WINDOW_HEIGHT, WINDOW_WIDTH

import threading
import time
from datetime import datetime
from socket_utils import socket_send
import socket


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.generalLayout = QVBoxLayout()
        self.generalLayout.setAlignment(Qt.AlignCenter)

        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

         # Make sure to pass in 'self' to the child widget for it to access parent to for methods and children
        self.mainWidget = MainContainer(self)

        self.setWindowTitle('Main Window')  # Sets name of window
        # Adds central widget where we are going to do most of our work
        self.setCentralWidget(self.mainWidget)
        self.setGeometry(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

    #TODO: fix server comm integration
    # def emit_message(self, message, data):
    #     if self.connected:
    #         self.sio.emit(message, data)
    #     else:
    #         print('Not connected to server')


def create_ui_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 32111))
    s.listen(1)
    return s


def stimOnsetOffset(s, window):
    client_socket, _ = s.accept()
    mainStack = window.mainWidget.findChild(QStackedWidget,"Main Widget")
    enterButton = window.mainWidget.findChild(ButtonContainer, "Enter Button")
    last_on_stimulus = None
    while True:
        if stopThread:
            break

        # OFFSET
        currWidget = mainStack.currentWidget()
        enterButton.stimuli.toggleOff()
        for button in currWidget.findChildren(ButtonContainer):
            button.stimuli.toggleOff()
        setStimuliStatus('off')
        x = getStatus()
        if last_on_stimulus is not None:
            x['on_stimulus_timestamp'] = last_on_stimulus
        else:
            x['on_stimulus_timestamp'] = None
        print(f"OFF STIMULUS: {datetime.now()}, Sending {x}")
        socket_send(sending_socket=client_socket, data=x)

        printStatus()
        time.sleep(5)

        if stopThread:
            break

        # ONSET
        currWidget = mainStack.currentWidget()
        enterButton.stimuli.toggleOn()
        for button in currWidget.findChildren(ButtonContainer):
            button.stimuli.toggleOn()
        setStimuliStatus('on')
        x = getStatus()
        last_on_stimulus = x['timestamp']

        print(f"ON STIMULUS: {datetime.now()}")
        print(f"Sending {x}")
        socket_send(sending_socket=client_socket, data=x)

        printStatus()
        time.sleep(5)


def webAppSocket(window):
    async def server(websocket):
        print("Client Connected")
        while True:
            text = await websocket.recv()
            if text.startswith("prompt: "):
                promptBox = window.mainWidget.findChild(QLabel, "Prompt")
                promptBox.setText(text[8:])
            elif text.startswith("disconnect"):
                print("Client Disconnected")
                break

    async def startServer():
        ip = socket.gethostbyname(socket.gethostname())
        port = 8765
        print(f"Starting ws server on {ip}:{port}")
        async with websockets.serve(server, ip, port):
            await asyncio.Future()

    asyncio.run(startServer())


def create_window():
    window = Window()
    window.setStyleSheet(windowStyle)
    window.show()
    print(f"window shown: {datetime.now()}")
    return window


def mainGUIFunc(client_socket, synch):
    # synch.wait()
    global stopThread
    stopThread = False
    app = QApplication(sys.argv)
    window = create_window()

    threading.Thread(target=stimOnsetOffset, args=(client_socket, window,)).start()

    # Thread for web app websocket
    threading.Thread(target=webAppSocket, args=(window,)).start()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        stopThread = True
        print('Closing Window ...')
