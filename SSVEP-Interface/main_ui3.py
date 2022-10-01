import sys
#import socketio
from PyQt5.QtCore import center, Qt
from PyQt5.QtGui import QFont

from PyQt5.QtWidgets import QApplication, QStackedWidget, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtWidgets import QMainWindow

from Pages.HomePage.homepage import HomePageWidget

from Pages.styles import windowStyle, navigationButtonStyle

class Home(QMainWindow):
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
        self.homePage = HomePageWidget(self)

        self.setWindowTitle('Main Window')  # Sets name of window
        # Adds central widget where we are going to do most of our work
        self.setCentralWidget(self.homePage)
        self.setGeometry(0, 0, 1600, 900)

    #TODO: fix server comm integration
    # def emit_message(self, message, data):
    #     if self.connected:
    #         self.sio.emit(message, data)
    #     else:
    #         print('Not connected to server')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Home()
    win.setStyleSheet(windowStyle)
    win.show()
    sys.exit(app.exec_())
