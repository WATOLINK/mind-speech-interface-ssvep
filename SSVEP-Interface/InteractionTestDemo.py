from concurrent.futures import thread
from http.client import ImproperConnectionState
import imp
import sys

from PyQt5.QtWidgets import QApplication,QVBoxLayout,QWidget,QHBoxLayout,QSizePolicy,QLineEdit,QLabel
from PyQt5.QtCore import QCoreApplication, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore

from Pages.styles import windowStyle,textBoxStyle
from Pages.button_container import ButtonContainer

from Pages.HomePage.homepage import promptBox

from InteractionTest.yesno import YesNoWidget
import random as r
import threading
import time
import socket
import pickle


class Window(QMainWindow):
    """Main Window."""

    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)


        self.setWindowTitle('Main Window')  # Sets name of window
        # Adds central widget where we are going to do most of our work

        self.setCentralWidget(HomePageWidget(self))
        
        self.centralWidget
        # Sets location (x, y) and size (width, height) of current window
        self.setGeometry(0, 0, 1600, 900)
        
        
    
    

# global par 

class HomePageWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        
        self.myThread = AThread()
        self.myThread.start()
        

        
        self.parent = parent 
        # global par
        # par = parent
        
        self.layout = QVBoxLayout()
        # self.testText = str(r.randint(1,20))
        self.testText = "bleh"
        
        
        self.layout.addWidget(promptBox(self.testText))
        self.layout.addWidget(inputBox(self))
        self.layout.addWidget(YesNoWidget(self))
        
        bottomLayout = QHBoxLayout()
        bottomLayout.setStretch(0, 1)
        bottomLayout.setStretch(1, 1)
        bottomLayout.setStretch(2, 1)
        
        # self.confirmButton = ButtonContainer("Confirm", horizontal=True, checkable=False, border=False)
        # self.confirmButton.clicked.connect(lambda: confirm(parent, "beepboop"))
        # confirmButton.setChecked(th)
        

        self.dummyWidget = QWidget()
        self.dummyWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        bottomLayout.addWidget(self.dummyWidget) # Dummy widget
        # bottomLayout.addWidget(self.confirmButton)
        bottomLayout.addWidget(self.dummyWidget) # Dummy widget

        self.layout.addLayout(bottomLayout)

        self.setLayout(self.layout)
        self.myThread.wait.connect(self.onWait)
        self.myThread.twoS.connect(self.onTwo)

        
    def onWait(self, wow):
        confirm(self.parent, str(wow))
    
    def onTwo(self, wow):
        lessThan(self.parent, str(wow))
        
        
       

def inputBox(parent):
    textbox = QLineEdit()
    textbox.setStyleSheet(textBoxStyle)
    textbox.setObjectName("Input")
    return textbox

def confirm(parent, sig):
    # print("entered")
    # print("signal num", sig)
    messageBox = parent.findChild(QLabel,"Prompt")
    inputField = parent.findChild(QLineEdit,"Input")
    currWidget = parent.findChild(QWidget, "YN Widget")


    messageBox.setText(sig)
    if inputField.text():
        temp = messageBox.text() + f"[{inputField.text()}]"
        messageBox.setText(sig)
        inputField.clear()
    

    for button in currWidget.findChildren(ButtonContainer):
        if button.isChecked():
            button.setChecked(False)

    # messageBox.update()
    # parent.update()

def lessThan(parent, sig):
    inputField = parent.findChild(QLineEdit,"Input")

    inputField.setText(sig)



def mainFuncTest():
    app = QApplication(sys.argv)
    win = Window()
    win.setStyleSheet(windowStyle)
    win.show()
    sys.exit(app.exec_())


class AThread(QThread):
    
    wait = pyqtSignal(str)
    twoS = pyqtSignal(str)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        self.s.connect(('127.0.0.1', 55432))
        count = 0
        while True:
            msg = self.s.recv(10000000)
            message = pickle.loads(msg)
            self.twoS.emit(str(message))

            print(message)
            # if int(message) == 8:
            #     x = "yes"
            #     self.wait.emit(x)
            # elif int(message) == 10:
            #     x = "no"
            #     self.wait.emit(x)
            # else:
                
            count = count + 1
            
            
            
        

            
    
