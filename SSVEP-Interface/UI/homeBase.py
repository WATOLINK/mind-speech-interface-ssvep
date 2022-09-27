from PyQt5.QtWidgets import QApplication,QVBoxLayout,QWidget,QHBoxLayout,QSizePolicy,QLineEdit,QLabel
from PyQt5.QtCore import QCoreApplication, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore

import socket
import pickle



class AThread(QThread):
    
    yesSig = pyqtSignal(float)
    noSig = pyqtSignal(float)
    badSig = pyqtSignal(float)
    testSig = pyqtSignal(float)

    enterButtonSig = pyqtSignal()
    keyboardPageSig = pyqtSignal()
    helpPageSig = pyqtSignal()
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        self.s.connect(('127.0.0.1', 55432))
        while True:
            try:
                msg = self.s.recv(10000000)
                message = pickle.loads(msg)
                # if float(message) == 14.75:
                #     self.yesSig.emit(message)
                # elif float(message) == 11.75:
                #     self.noSig.emit(message)
                # elif float(message) == 1.1:
                #     self.testSig.emit(message)
                # else:
                # self.badSig.emit(message)
                
                self.enterButtonSig.emit()
                self.keyboardPageSig.emit()
                self.helpPageSig.emit()

                print(message)
                    
            except EOFError:
                    continue


    