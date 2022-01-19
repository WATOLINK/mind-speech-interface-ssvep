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

from Embedded_Server import Cyton_Board_Config, Cyton_Board_End

# Constants that must match constant declaration in sembedded script
HOST = '127.0.0.1'  # Server hostname or IP
PORT = 65432        # Port used by server

# Variables to change parameters of the test
START_DELAY_S = 5 # Seconds
NUM_TRIALS = 1
INDICATOR_TIME_VALUE_S = 5 # Seconds
TRIAL_BREAK_TIME = 10
STIM_PERIOD_TRIALS = 2
COL = ['Timestamp','Count','Ch1','Ch2','Ch3','Ch4','Ch5','Ch6','Ch7','Ch8','Ch9','Ch10','Ch11','Ch12','Ch13','Ch14','Ch15','Ch16']

data = []
color_code_order = []
color_freq_order = []
timestamp = []

def thread_function(stop, board, args):
    data_index = 0

    f = open("ODC-DEMO/demo_data/" + filename + ".txt", 'a')  # modify depending on CWD
    f.write(f"Session at {datetime.datetime.now()}\n\n")

    time.sleep(2)
    startDelay = START_DELAY_S
    for x in range(startDelay):
        label.setText(labelTxt(f"Starting in {str(startDelay-x)}"))
        time.sleep(1)
    order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    for trial in range(NUM_TRIALS):  # number of trials (5 times)
        print("=====Trial "+str(trial+1)+"=====")
        f.write("\n=====Trial "+str(trial+1)+"=====\n")
        
        # each trial will have a different order of stimulus
        random.shuffle(order)
        print(order)

        for stimPeriod in range(STIM_PERIOD_TRIALS):

            # just for testing otherwise the thread keeps running if you close the window
            if stop():
                break

            currentStim = stim[order[stimPeriod]]
            

            # indicate stimuli to focus on / display indicator
            currentStim.toggleIndicator(True)

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

            for x in range(int(INDICATOR_TIME_VALUE_S)):
                label.setText(
                    labelTxt(f"Keep you eyes where the red circle is. ({INDICATOR_TIME_VALUE_S-x})"))
                time.sleep(1)
            label.setText(labelTxt("Keep you eyes where the red circle was."))

            # start simulation period (all stimulis flashing)
            currentStim.toggleIndicator(False)

            
            for x in range(STIM_PERIOD_TRIALS):
                stim[x].toggleOn()
            
            start_time = time.time()
            board.start_stream(45000, args)
            time.sleep(5)  # set length of simulation period (5s)
            data.append(board.get_board_data().transpose()[:,0:17])   # get all data and remove it from internal buffer   
            board.stop_stream()
            
  
            # turn off all stimuli and prepare for next trial
            for x in range(STIM_PERIOD_TRIALS):
                stim[x].toggleOff()

        
            # Corresponding timestamp creation
            session_timestamp = []
            timestamp_rows = np.shape(data[data_index])[0] 

            # One-time millisecond extraction
            ms = repr(start_time).split('.')[1][:3]

            for each_timestamp_index in range(timestamp_rows):

                # Convert Unix time to desired timestamp format
                formatted_start_time = time.strftime("%Y-%m-%d %H:%M:%S.{} %Z".format(ms), time.localtime(start_time))
                session_timestamp.append( formatted_start_time )
                
                # Add 8ms to formatted_start_time 
                ms = int(ms) + 8

                # Work-around for floating point error from adding 8 ms
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

            timestamp.append(session_timestamp)
            data_index += 1            

        # just for testing otherwise the thread keeps running if you close the window
        if stop():
            break

        for x in range(int(TRIAL_BREAK_TIME)):
            label.setText(
                labelTxt(f"Time before next trial: ({TRIAL_BREAK_TIME-x})"))
            time.sleep(1)

    print("all trials finished")
    f.write("Session finished.\n\n")
    f.close()
    

    print('KEVIN 1      ', len(color_code_order), color_code_order[:6] )
    print('KEVIN 2     ', len(color_freq_order),  color_freq_order[:6] )
    post_process(data, timestamp)

    for i in range(len(data)):
        data[i] = pd.DataFrame(data[i], columns=COL)
    df = pd.concat(data)

    colour_freq_process(df)

    df.to_csv("ODC-DEMO/demo_data/" + filename + ".csv")

    Cyton_Board_End(board)

def labelTxt(text):
    return f'<h1 style="text-align:center; color: white">{text}</h1>'

def post_process( data, timestamp ):
    for i in range(np.shape( timestamp )[0]):
        data[i] = np.c_[ timestamp[i] , data[i]  ]

def colour_freq_process(df):
    # Handles color code and frequency
    print(df['Count'][0])
    index_epoch_list = df.index[df['Count'].astype(float) == 0.0].tolist()
    print('TEST LIST SIZES    ', len(index_epoch_list), len(color_code_order), len(color_freq_order))
    for i in range(len(index_epoch_list)):
        print(i)
        # Color code order going out of range
        df.loc[index_epoch_list[i], 'Color Code'] = color_code_order[i]
        df.loc[index_epoch_list[i], 'Frequency'] = color_freq_order[i]

    
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
        self.gridLayout = QGridLayout(self.frame)
        for row in range(3):
            for col in range(4):
                stimNum = row*4+col
                stim[stimNum].toggleOff()
                self.gridLayout.addWidget(stim[stimNum], row+3, col*2)
        self.gridLayout.setSpacing(225)

    # resizes grid during window resize
    def resizeEvent(self, event): 
        super().resizeEvent(event)

        l = min(self.width(), self.height())
        center = self.rect().center()

        rect = QRect(0, 0, int(l*(5/3)), l) # 5 x 3 ratio
        rect.moveCenter(center)
        self.frame.setGeometry(rect)

        self.gridLayout.setColumnMinimumWidth(1, int(l/12)) # 3 additional columns fill space to make it a 4x3 grid 
        self.gridLayout.setColumnMinimumWidth(3, int(l/12))
        self.gridLayout.setColumnMinimumWidth(5, int(l/12))


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

    global label
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
    x = threading.Thread(target=thread_function, args=(lambda: stopThread, board_details[0], board_details[1]))
    x.start()

    window.resize(1600, 1200) # initial window size
    window.show()
    
    try:
        sys.exit(app.exec_())
    except SystemExit:
        stopThread = True
        file.close()
        print('Closing Window...')

