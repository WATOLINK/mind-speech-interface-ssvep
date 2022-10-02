from concurrent.futures import thread
from http.client import ImproperConnectionState
# import imp
import sys

from PyQt5.QtWidgets import QApplication,QVBoxLayout,QWidget,QHBoxLayout,QSizePolicy,QLineEdit,QLabel
from PyQt5.QtCore import QCoreApplication, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore

from UI.styles import windowStyle,textBoxStyle
from UI.Components.button_container import ButtonContainer

from UI.MainWidget.mainWidget import promptBox

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
        self.setGeometry(0, 0, 2400, 1360)
        
        
    
    

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
        self.testText = "testing"
        
        
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
        self.myThread.yesSig.connect(self.onYes)
        self.myThread.noSig.connect(self.onNo)
        self.myThread.badSig.connect(self.onBad)

        
    def onBad(self, msg):
        showBad(self.parent, str(msg))
    
    def onNo(self):
        showNo(self.parent)
    
    def onYes(self):
        showYes(self.parent)
        
        
       
def showYes(parent):
    inputField = parent.findChild(QLineEdit,"Input")
    currWidget = parent.findChild(QWidget, "YN Widget")

    for button in currWidget.findChildren(ButtonContainer):
        print(button.label.text())
        if button.label.text() == "YES": 
            button.setChecked(True)
            inputField.setText("YES")
        elif button.label.text() == "NO":
            button.setChecked(False)

def showNo(parent):
    inputField = parent.findChild(QLineEdit,"Input")
    currWidget = parent.findChild(QWidget, "YN Widget")

    for button in currWidget.findChildren(ButtonContainer):
        print(button.label.text())
        if button.label.text() == "NO": 
            button.setChecked(True)
            inputField.setText("NO")
        elif button.label.text() == "YES":
            button.setChecked(False)

def showBad(parent, msg):
    inputField = parent.findChild(QLineEdit,"Input")
    currWidget = parent.findChild(QWidget, "YN Widget")

    for button in currWidget.findChildren(ButtonContainer):
        print(button.label.text())
        button.setChecked(False)

    inputField.setText(msg)


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



def mainFuncTest():
    app = QApplication(sys.argv)
    win = Window()
    win.setStyleSheet(windowStyle)
    win.setFixedSize(2400, 1360) # initial window size
    win.show()
    sys.exit(app.exec_())


class AThread(QThread):
    
    yesSig = pyqtSignal(float)
    noSig = pyqtSignal(float)
    badSig = pyqtSignal(float)
    
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        self.s.connect(('127.0.0.1', 55432))
        while True:
            try:
                msg = self.s.recv(10000000)
                message = pickle.loads(msg)
                if float(message) == 14.75:
                    self.yesSig.emit(message)
                elif float(message) == 11.75:
                    self.noSig.emit(message)
                else:
                    self.badSig.emit(message)

                print(message)
                    
            except EOFError:
                    continue
        
            
            
        

            
    
