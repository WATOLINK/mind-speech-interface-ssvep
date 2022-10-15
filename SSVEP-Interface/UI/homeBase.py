
from PyQt5.QtWidgets import QApplication,QVBoxLayout,QWidget,QHBoxLayout,QSizePolicy,QLineEdit,QLabel
from PyQt5.QtCore import QCoreApplication, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore

import socket
import pickle
import time
from UI.UI_DEFS import MAIN_STIM_FREQUENCIES


class AThread(QThread):
    
    yesSig = pyqtSignal()
    noSig = pyqtSignal()

    enterButtonSig = pyqtSignal()
    helpPageSig = pyqtSignal()
    returnHomeSig = pyqtSignal()

    voicePageSig = pyqtSignal()
    twitterPageSig = pyqtSignal()

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
                if MAIN_STIM_FREQUENCIES['Enter'] == freq:
                    self.enterButtonSig.emit()
                elif page == "Output Menu Page":
                    if freq == MAIN_STIM_FREQUENCIES['Output Menu 1']:
                        self.twitterPageSig.emit()
                    elif freq == MAIN_STIM_FREQUENCIES['Output Menu 2']:
                        self.voicePageSig.emit()
                    elif freq == MAIN_STIM_FREQUENCIES['Output Menu Help']:
                        self.helpPageSig.emit()
                elif page == "Keyboard YN Menu Page":
                    if freq == MAIN_STIM_FREQUENCIES['Keyboard YN Menu 1']:
                        self.keyboardPageSig.emit()
                    elif freq == MAIN_STIM_FREQUENCIES['Keyboard YN Menu 2']:
                        self.ynPageSig.emit()
                    elif freq == MAIN_STIM_FREQUENCIES['Back to Output Menu']:
                        self.returnHomeSig.emit()
                elif page == "YN Page":
                    if freq == MAIN_STIM_FREQUENCIES['YN 1']:
                        self.yesSig.emit()
                    elif freq == MAIN_STIM_FREQUENCIES['YN 2']:
                        self.noSig.emit()
                elif page == "Keyboard Page":
                    if freq == MAIN_STIM_FREQUENCIES['Keyboard 1']:
                        self.keyboardUpButOne.emit()
                    elif freq == MAIN_STIM_FREQUENCIES['Keyboard 2']:
                        self.keyboardUpButTwo.emit()
                    elif freq == MAIN_STIM_FREQUENCIES['Keyboard 3']:
                        self.keyboardUpButThree.emit() 
                    elif freq == MAIN_STIM_FREQUENCIES['Keyboard 4']:
                        self.keyboardUpButFour.emit()
                    elif freq == MAIN_STIM_FREQUENCIES['Space']:
                        self.spaceSig.emit()
                    elif freq == MAIN_STIM_FREQUENCIES['Backspace']:
                        self.backspaceSig.emit()
                    elif freq == MAIN_STIM_FREQUENCIES['Word Toggle']:
                        self.toggleSig.emit()
                    
            except EOFError:
                continue
