
from PyQt5.QtWidgets import QApplication,QVBoxLayout,QWidget,QHBoxLayout,QSizePolicy,QLineEdit,QLabel
from PyQt5.QtCore import QCoreApplication, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore

import socket
import pickle
import time


class AThread(QThread):
    
    yesSig = pyqtSignal()
    noSig = pyqtSignal()

    enterButtonSig = pyqtSignal()
    helpPageSig = pyqtSignal()
    returnHomeSig = pyqtSignal()

    voicePageSig = pyqtSignal()
    twitterPageSig = pyqtSignal()
    visCommPageSig = pyqtSignal()

    keyboardPageSig = pyqtSignal()
    ynPageSig = pyqtSignal()

    keyboardUpButOne = pyqtSignal()
    keyboardUpButTwo = pyqtSignal()
    keyboardUpButThree = pyqtSignal()
    keyboardUpButFour = pyqtSignal()

    spaceSig = pyqtSignal()
    backspaceSig = pyqtSignal()
    toggleSig = pyqtSignal()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        self.s.connect(('127.0.0.1', 55432))
        while True:
            try:
                msg = self.s.recv(10000000)
                message = pickle.loads(msg)
                
                freq = message["freq"]
                page = message["page"]
                
                print(freq)
                print(page)
                if freq == 8.25:
                    self.enterButtonSig.emit()

                if page == "Output Menu Page":
                    if freq == 13.75:
                        self.twitterPageSig.emit()
                    elif freq == 11.75:
                        self.voicePageSig.emit()
                    elif freq == 9.75:
                        self.visCommPageSig.emit()
                    elif freq == 14.25:
                        self.helpPageSig.emit()

                if page == "Keyboard YN Menu Page":
                    if freq == 12.75:
                        self.keyboardPageSig.emit()
                    elif freq == 13.75:
                        self.ynPageSig.emit()
                    elif freq == 14.25:
                        self.helpPageSig.emit()
                    elif freq == 10.75:
                        self.returnHomeSig.emit()

                if page == "YN Page":
                    if freq == 8.75:
                        self.yesSig.emit()
                    elif freq == 13.75:
                        self.noSig.emit()

                if page == "Keyboard Page":
                    if freq == 12.75:
                        self.keyboardUpButOne.emit()
                    elif freq == 11.75:
                        self.keyboardUpButTwo.emit()
                    elif freq == 9.75:
                        self.keyboardUpButThree.emit() 
                    elif freq == 10.75:
                        self.keyboardUpButFour.emit()
                    elif freq == 8.75:
                        self.spaceSig.emit()
                    elif freq == 13.75:
                        self.backspaceSig.emit()
                    elif freq == 14.25:
                        self.toggleSig.emit()
                    
            except EOFError:
                    continue


    