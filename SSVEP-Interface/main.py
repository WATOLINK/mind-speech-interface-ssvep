import sys
# import socketio
from PyQt5.QtCore import center, Qt

from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QMainWindow, QStackedWidget

from UI.MainWidget.mainWidget import MainContainer

from UI.styles import windowStyle

from UI.Components.button_container import  ButtonContainer

import threading
import time

class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        #TODO: fix server comm integration
        # SocketIO connection
        # self.connected = False
        # self.sio = socketio.Client()
        # try:
        #     self.sio.connect('http://127.0.0.1:5000')
        #     print("Connected")
        #     self.connected = True
        # except socketio.exceptions.ConnectionError as err:
        #     print("ConnectionError:", err)

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
        self.setGeometry(0, 0, 2400, 1340)

    #TODO: fix server comm integration
    # def emit_message(self, message, data):
    #     if self.connected:
    #         self.sio.emit(message, data)
    #     else:
    #         print('Not connected to server')



def stimOnsetOffset():
    mainStack = window.mainWidget.findChild(QStackedWidget,"Main Widget")
    enterButton = window.mainWidget.findChild(ButtonContainer, "Enter Button")
    
    while True:
        if stopThread:
            print("Exiting Stim Controller ...")
            break

        #ONSET
        currWidget = mainStack.currentWidget()
        enterButton.stimuli.toggleOn()
        for button in currWidget.findChildren(ButtonContainer):
            button.stimuli.toggleOn()

        print(f"Stim on, Page: {currWidget.objectName()}")
        
        time.sleep(2)

        if stopThread:
            print("exiting stim controller thread")
            break

        currWidget = mainStack.currentWidget()
        enterButton.stimuli.toggleOff()
        for button in currWidget.findChildren(ButtonContainer):
            button.stimuli.toggleOff()
        print(f"Stim off")

        time.sleep(2)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    global window
    window = Window()
    window.setStyleSheet(windowStyle)

    global stopThread
    stopThread = False
    x = threading.Thread(target=stimOnsetOffset)
    x.start()

    window.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        stopThread = True
        print('Closing Window ...')
