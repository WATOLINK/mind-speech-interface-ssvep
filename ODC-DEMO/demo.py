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

from Embedded_Server import Cyton_Board_Config, Cyton_Board_End

# Constants that must match constant declaration in sembedded script
HOST = '127.0.0.1'  # Server hostname or IP
PORT = 65432        # Port used by server
col = ['Count','Ch1','Ch2','Ch3','Ch4','Ch5','Ch6','Ch7','Ch8','Ch9','Ch10','Ch11','Ch12','Ch13','Ch14','Ch15','Ch16']
data = []

def thread_function(stop, board, args):
    f = open("ODC-DEMO/"+ filename, 'a')  # modify depending on CWD
    f.write(f"Session at {datetime.datetime.now()}\n\n")
    print("starting")

    time.sleep(2)
    startDelay = 10
    for x in range(startDelay):
        label.setText(labelTxt(f"Starting in {str(startDelay-x)}"))
        time.sleep(1)

    order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    for trial in range(2):  # number of trials (5 times)
        print("=====Trial "+str(trial+1)+"=====")
        f.write("\n=====Trial "+str(trial+1)+"=====\n")

        # each trial will have a different order of stimulus
        random.shuffle(order)
        print(order)

        for stimPeriod in range(12):

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

            indicatorTime = 5

            for x in range(int(indicatorTime)):
                label.setText(
                    labelTxt(f"Keep you eyes where the red circle is. ({indicatorTime-x})"))
                time.sleep(1)
            label.setText(labelTxt("Keep you eyes where the red circle was."))

            # start simulation period (all stimulis flashing)
            currentStim.toggleIndicator(False)

            
            for x in range(12):
                stim[x].toggleOn()
                
            board.start_stream(45000, args)
            time.sleep(5)  # set length of simulation period (5s)
    
            data.append(board.get_board_data().transpose()[:,1:17])   # get all data and remove it from internal buffer            
            board.stop_stream()
  
            # turn off all stimuli and prepare for next trial
            for x in range(12):
                stim[x].toggleOff()

            

        # just for testing otherwise the thread keeps running if you close the window
        if stop():
            break

        trialBreakTime = 120

        for x in range(int(trialBreakTime)):
            label.setText(
                labelTxt(f"Time before next trial: ({trialBreakTime-x})"))
            time.sleep(1)

    print("all trials finished")
    f.write("Session finished.\n\n")
    f.close()
    
    for i in range(len(data)):
        data[i] = pd.DataFrame(data[i], columns=col)
    df = pd.concat(data)
    df.to_csv(filename + ".csv")

def labelTxt(text):
    return f'<h1 style="text-align:center; color: white">{text}</h1>'


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

        rect = QRect(0, 0, l*(5/3), l) # 5 x 3 ratio
        rect.moveCenter(center)
        self.frame.setGeometry(rect)

        self.gridLayout.setColumnMinimumWidth(1, l/12) # 3 additional columns fill space to make it a 4x3 grid 
        self.gridLayout.setColumnMinimumWidth(3, l/12)
        self.gridLayout.setColumnMinimumWidth(5, l/12)


if __name__ == '__main__':


    # File and GUI config
    x = datetime.datetime.now()

    global filename 
    filename =  f"{x.strftime('%j')}_{x.strftime('%Y')}_{x.strftime('%f')}.txt" #day of year, year, millisecond

    file = open("ODC-DEMO/"+ filename, "x") # create log 

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

    # BCI Config
    board_details = Cyton_Board_Config(True)

    stopThread = False
    x = threading.Thread(target=thread_function, args=(lambda: stopThread, board_details[0], board_details[1]))
    x.start()

    window.resize(1600, 1200) # initial window size
    window.show()
    
    try:
        Cyton_Board_End()
        sys.exit(app.exec_())
    except SystemExit:
        stopThread = True
        file.close()
        print('Closing Window...')

