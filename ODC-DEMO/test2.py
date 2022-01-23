from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QWidget,
    QGridLayout,
    QFrame,
    QVBoxLayout,
)
from PyQt5.QtCore import QRect
import sys, random, threading, datetime, time
import circle_stimuli as Stim
import numpy as np
import pandas as pd
import os
from demo import labelTxt, Stimuli

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle('Flashing Stim 1')
    window.setStyleSheet("background-color: black;")

    layout = QVBoxLayout()

    global label
    label = QLabel(labelTxt("ODC-DEMO"))
    label.setFixedHeight(100)
    layout.addWidget(label)
    grid = Stimuli() # stimuli grid widget
    
    layout.addWidget(grid)
    window.setLayout(layout)
    
    # window.resize(1600, 1200) # initial window size
    window.show()
    sys.exit(app.exec_())

