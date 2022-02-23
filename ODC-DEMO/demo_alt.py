from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QWidget,
    QGridLayout,
    QFrame,
    QVBoxLayout
)
from PyQt5.QtCore import QRect,Qt
from PyQt5.QtGui import QPainter, QBrush, QPen
import sys, random, threading, datetime
import circle_stimuli as Stim
import numpy as np
import pandas as pd
import os
from time import time, sleep, strftime, localtime

from Embedded_Server import Cyton_Board_Config, Cyton_Board_End

# Variables to change parameters of the test
START_DELAY_S = 1 # 20 Seconds
NUM_TRIALS = 1 # 5 Trials
INDICATOR_TIME_VALUE_S = 1 # 5 Seconds
TRIAL_BREAK_TIME = 5 # 120 seconds 
STIM_PERIOD_TRIALS = 12 # 12 for the 12 stimuli per trial

color_code_order = []
color_freq_order = []
timestamp = []

def display_procedure(stop, board, args):
    f = open("ODC-DEMO/demo_data/" + filename + ".txt", 'a')  # modify depending on CWD
    f.write(f"Session at {datetime.datetime.now()}\n\n")
    board.start_stream(70000, args)
    
    # Test 
    ti = time()

    sleep(1)
    startDelay = START_DELAY_S
    for x in range(startDelay):
        label.setText(labelTxt(f"Starting in {str(startDelay-x)}"))
        sleep(1)
    order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    for trial in range(NUM_TRIALS):  # number of trials (5 times)
        print("=====Trial "+str(trial+1)+"=====")
        f.write("\n=====Trial "+str(trial+1)+"=====\n")
        
        # each trial will have a different order of stimulus
        random.shuffle(order)
        print(order)

        timestamp.append(time())
        board.insert_marker(0.666)

        for stimPeriod in range(STIM_PERIOD_TRIALS):
            # just for testing otherwise the thread keeps running if you close the window
            if stop():
                break
            currentStim = stim[order[stimPeriod]]
            stimLabel = preStimIndicators[order[stimPeriod]]

            # log color and hz to terminal
            color = str(currentStim.rValue)+"," + \
                str(currentStim.gValue)+","+str(currentStim.bValue)
            if color == "255,255,255":
                color = "white"
                colorCode = "01"
            elif color == "0,0,255":
                color = "blue"
                colorCode = "02"
            elif color == "0,255,0":
                color = "green"
                colorCode = "03"
            print(f"{color}\t{currentStim.freqHertz}Hz")

            # log code to file
            f.write(f"{currentStim.id:02} " + colorCode +
                    f" {currentStim.freqHertz:02}\n")
            color_code_order.append(colorCode)
            color_freq_order.append(currentStim.freqHertz)

            # indicate stimuli to focus on / display indicator
            currentStim.toggleIndicator(True)
            label.setText(labelTxt(f"Keep you eyes where the red circle is."))
            
            for x in range(int(INDICATOR_TIME_VALUE_S)):
                stimLabel.setText(labelTxt(str(INDICATOR_TIME_VALUE_S - x)))
                sleep(1)
            stimLabel.setText(labelTxt(""))
            
            currentStim.toggleIndicator(False)

            timestamp.append(time())
            board.insert_marker(0.666)
            
            for x in range(STIM_PERIOD_TRIALS):
                stim[x].toggleOn()
        
            sleep(5)  # set length of simulation period (5s)
            timestamp.append(time())
            board.insert_marker(0.666)

            # turn off all stimuli and prepare for next trial
            for x in range(STIM_PERIOD_TRIALS):
                stim[x].toggleOff()

        # just for testing otherwise the thread keeps running if you close the window
        if stop():
            break
        for x in range(int(TRIAL_BREAK_TIME)):
            label.setText(
                labelTxt(f"Time before next trial: ({TRIAL_BREAK_TIME-x})"))
            sleep(1)
        
    label.setText(
                labelTxt(f"Trials finished"))
    print("all trials finished")
    f.write("Session finished.\n\n")
    f.close()
    data = board.get_board_data().transpose() 
    board.stop_stream()
    duration = time()-ti
    generate_test_report(board, duration, data, timestamp, color_code_order, color_freq_order)

    try:
        df = pd.DataFrame(data)
        df.to_csv("ODC-DEMO/test_data.csv", index=False)
    except:
        print('Post data processing and CSV Export failed')
    finally:
        Cyton_Board_End(board)

def labelTxt(text):
    return f'<h1 style="text-align:center; color: white">{text}</h1>'

def generate_test_report(board, duration, data, timestamp, color_code_order, color_freq_order):
    tf = open("ODC-DEMO/test_report.txt", 'w')  
    tf.write("Data list len: ")
    tf.write(str(np.shape(data)))
    tf.write("\n")
    tf.write("Start time list len: ")
    tf.write(str(len(timestamp))) 
    tf.write("\n")
    tf.write("CC list len: ")
    tf.write(str(len(color_code_order)))
    tf.write("\n")
    tf.write("CF list len: ")
    tf.write(str(len(color_freq_order)))
    tf.write("\n\n")
    tf.write("Marker channel: ")
    tf.write(str(board.get_marker_channel(0)))
    tf.write("\n\n")
    tf.write("Sampling duration: ")
    tf.write(str(duration))
    tf.write("\n\n")
    tf.write("Expected Samples: ")
    tf.write(str(250*duration)) 
    tf.write("\n")
    tf.write("Received Samples: ")
    tf.write(str(np.shape(data)[0]))
    tf.write("\n")
    tf.close()

class Stimuli(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1200, 900)

        self.frame = QFrame(self, objectName="frame") # ensures correct aspect ratio of grid
        global stim
        stim = []

        # white stims
        stim.append(Stim.CircleFlash(20, 255, 255, 255, 1))
        stim.append(Stim.CircleFlash(18, 255, 255, 255, 2))
        stim.append(Stim.CircleFlash(16, 255, 255, 255, 3))
        stim.append(Stim.CircleFlash(14, 255, 255, 255, 4))
        stim.append(Stim.CircleFlash(12, 255, 255, 255, 5))
        stim.append(Stim.CircleFlash(10, 255, 255, 255, 6))
        stim.append(Stim.CircleFlash(8, 255, 255, 255, 7))
        stim.append(Stim.CircleFlash(6, 255, 255, 255, 8))

        # blue stims
        stim.append(Stim.CircleFlash(11, 0, 0, 255, 9))
        stim.append(Stim.CircleFlash(7, 0, 0, 255, 10))

        # green stims
        stim.append(Stim.CircleFlash(9, 0, 255, 0, 11))
        stim.append(Stim.CircleFlash(5, 0, 255, 0, 12))

        # append stimulis to grid in random order
        random.shuffle(stim)

        # create array of indicators
        global preStimIndicators
        preStimIndicators = []
        for x in range(12):
            preStim = QLabel(labelTxt(""))
            preStimIndicators.append(preStim)
            
        self.gridLayout = QGridLayout(self.frame)
        # self.gridLayout.addWidget(QLabel(), 3, 0)
        for row in range(3):
            for col in range(4):
                stimNum = row*4+col

                self.gridLayout.addWidget(preStimIndicators[stimNum], row*2+3, col*2)
                if (col != 3):
                    self.gridLayout.addWidget(QLabel(), row*2+3, col*2+1)

                stim[stimNum].toggleOff()
                self.gridLayout.addWidget(stim[stimNum], row*2+4, col*2)
        self.gridLayout.setSpacing(10)

    # resizes grid during window resize
    def resizeEvent(self, event): 
        super().resizeEvent(event)

        l = min(self.width(), self.height())
        center = self.rect().center()

        rect = QRect(0, 0, int(l*(7/6)), l) # 5 x 3 ratio
        rect.moveCenter(center)
        self.frame.setGeometry(rect)

        # self.gridLayout.setColumnMinimumWidth(1, int(l/12)) # 3 additional columns fill space to make it a 4x3 grid 
        # self.gridLayout.setColumnMinimumWidth(3, int(l/12))
        # self.gridLayout.setColumnMinimumWidth(5, int(l/12))

if __name__ == '__main__':
    # File and GUI config
    x = datetime.datetime.now()

    global filename 
    filename =  f"{x.strftime('%j')}_{x.strftime('%Y')}_{x.strftime('%f')}" #day of year, year, millisecond

    file = open("ODC-DEMO/demo_data/" + filename + ".txt", "x") # create log 

    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle('Flashing Stim 1')
    window.setStyleSheet("background-color: black;")

    layout = QVBoxLayout()

    # global label
    label = QLabel(labelTxt("ODC-DEMO"))
    label.setFixedHeight(100)
    layout.addWidget(label)
    print("Test")
    grid = Stimuli() # stimuli grid widget
    
    layout.addWidget(grid)
    window.setLayout(layout)
    
    # BCI Config
    board_details = Cyton_Board_Config(False)
    stopThread = False
    x = threading.Thread(target=display_procedure, args=(lambda: stopThread, board_details[0], board_details[1]))
    x.start()

    window.setFixedSize(1000, 900) # initial window size
    window.show()
    
    try:
        sys.exit(app.exec_())
    except SystemExit:
        stopThread = True
        file.close()
        print('Closing Window...')

