from turtle import color
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

from flask import session
import circle_stimuli as Stim
import numpy as np
import pandas as pd
import os
from time import time, sleep, strftime, localtime

from Embedded_Server import Cyton_Board_Config, Cyton_Board_End

# Variables to change parameters of the test
START_DELAY_S = 1 # 20 Seconds
NUM_TRIALS = 2 # 5 Trials
INDICATOR_TIME_VALUE_S = 1 # 5 Seconds
TRIAL_BREAK_TIME = 1 # 120 seconds 
STIM_PERIOD_TRIALS = 12 # 12 for the 12 stimuli per trial

data = []
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

        data.append(board.get_board_data().transpose()[:,1:9]) # get data at start AS WELL AS BETWEEN TRIALS
        timestamp.append(time())

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

            data.append(board.get_board_data().transpose()[:,1:9])   # get all data for in between flashes (null)
            timestamp.append(time())
            
            for x in range(STIM_PERIOD_TRIALS):
                stim[x].toggleOn()
        
            sleep(5)  # set length of simulation period (5s)
            data.append(board.get_board_data().transpose()[:,1:9])   # get all data for stimuli flash (individual)   
            timestamp.append(time())

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

    board.stop_stream()
    duration = time()-ti
    generate_test_report(board, duration, data, timestamp, color_code_order, color_freq_order)

    try:
        df = post_process(data, timestamp, color_code_order, color_freq_order)
        df.to_csv("ODC-DEMO/demo_data/" + filename + ".csv", index=False)
    except:
        print('Post data processing and CSV Export failed')
    finally:
        Cyton_Board_End(board)

def labelTxt(text):
    return f'<h1 style="text-align:center; color: white">{text}</h1>'

def post_process( data, timestamp, color_code, color_freq ):
    for data_block_index in range(len(data)):
        data_rows, data_cols = np.shape(data[data_block_index])
        start_time = timestamp[data_block_index]

        # Extract down to milliseconds
        ms = repr(start_time).split('.')[1][:3]
        # Corresponding timestamp creation
        block_timestamp = []
    
        for time_increment_index in range(data_rows):
            # Convert Unix time to desired timestamp format
            formatted_start_time = strftime("%Y-%m-%d %H:%M:%S.{} %Z".format(ms), localtime(start_time))[:23]
            block_timestamp.append( formatted_start_time )

            # Increment by 4ms for 250Hz
            # Increment by 8ms for 125Hz
            ms = int(ms) + 4
            # Work-around for floating point error from adding millisecond
            if ms > 999:
                rem_ms = str(ms - 1000)
                start_time += 1  
                ms = '00' + rem_ms
            else:
                ms = str(ms)
                if len(str(ms)) == 1: 
                    ms = '00' + ms
                elif len(str(ms)) == 2:
                    ms = '0' + ms
                else:
                    pass       

        # Update timestamp list to contain incremented timestamp block instead of start time
        timestamp[ data_block_index ] = block_timestamp
        
    # Create header row
    header = ['Time']
    for i in range(1, 9):
        header.append('CH{}'.format(i))

    # Put timestamp, color code, and frequency columns together with data blocks
    for i in range(len(data)):
        data[i] = np.c_[ timestamp[i], data[i] ]
        data[i] = pd.DataFrame(data[i], columns=header)
 
    main_ctr = 0
    session_ctr = 0
    done_adding_cols = False
    is_two_block = True
    is_stimulus_session = False
    while not done_adding_cols:
        if is_two_block and not is_stimulus_session:
            data[main_ctr].loc[0, 'Color Code'] = 0
            data[main_ctr].loc[0, 'Frequency'] = 0

            data[main_ctr + 1].loc[0, 'Color Code'] = 0
            data[main_ctr + 1].loc[0, 'Frequency'] = 0       
            
            main_ctr += 2
            is_two_block = False
            is_stimulus_session = True

        if not is_two_block and is_stimulus_session:
            data[main_ctr].loc[0, 'Color Code'] = color_code[session_ctr]
            data[main_ctr].loc[0, 'Frequency'] = color_freq[session_ctr]

            main_ctr += 1
            session_ctr += 1
            if session_ctr == STIM_PERIOD_TRIALS:
                is_two_block = True
            is_stimulus_session = False

            if main_ctr == (len(data)) and session_ctr == (len(color_code)):
                is_stimulus_session = True
                done_adding_cols = True

        if not is_two_block and not is_stimulus_session:
            data[main_ctr].loc[0, 'Color Code'] = 0
            data[main_ctr].loc[0, 'Frequency'] = 0
            main_ctr += 1
            is_stimulus_session = True
        
    # Convert to 1 DataFrame
    df_all = pd.concat(data)
    #df_all.index.name = 'Count'
    return df_all

def generate_test_report(board, duration, data, timestamp, color_code_order, color_freq_order):
    tf = open("ODC-DEMO/test_report.txt", 'w')  
    tf.write("Size of Data List: ")
    tf.write(str(len(data)))
    tf.write("\n")
    tf.write("Size of Start Time List: ")
    tf.write(str(len(timestamp))) 
    tf.write("\n")
    tf.write("Size of Color Code List: ")
    tf.write(str(len(color_code_order)))
    tf.write("\n")
    tf.write("Size of Color Freq List: ")
    tf.write(str(len(color_freq_order)))
    tf.write("\n")
    tf.write("Marker Channel: ")
    tf.write(str(board.get_marker_channel(-1)))
    tf.write("\n")
    tf.write("Data Acquisition Duration: ")
    tf.write(str(duration))
    tf.write("\n\n")
    total_data_count = 0
    for i in data:
        tf.write(str(np.shape(i)))
        tf.write("\n")
        total_data_count += np.shape(i)[0]
    tf.write("\n\n")
    tf.write("Expected Samples: ")
    tf.write(str(250*duration)) 
    tf.write("\n")
    tf.write("Received Samples: ")
    tf.write(str(total_data_count))
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

