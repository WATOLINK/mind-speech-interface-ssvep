from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QWidget,
    QGridLayout,
)
import threading
import random
import time
import datetime
import circle_stimuli as Stim
import sys
import os
# might to change following line fron where you are in the repo, works for me but might not on another workspace? - Ivan
sys.path.append(os.path.abspath(
    'mind-speech-interface-ssvep/SSVEP-Interface/Pages'))


def thread_function(stop):
    f = open("ODC-DEMO/log.txt", 'a')  # modify depending on CWD
    f.write(f"Session at {datetime.datetime.now()}\n\n")
    print("start")

    order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    for trial in range(5):  # number of trials (5 times)
        print("=====Trial "+str(trial+1)+"=====")
        f.write("\n=====Trial "+str(trial+1)+"=====\n")

        # each trial will have a different order of stimulus
        random.shuffle(order)
        print(order)

        for stimPeriod in range(12):

            # just for testing otherwise the thread keeps running if you close the window
            if stop():
                print("thread ended")
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

            time.sleep(0.5)  # time indicator is displayed (4s)

            # start simulation period (all stimulis flashing)
            currentStim.toggleIndicator(False)
            for x in range(12):
                stim[x].toggleOn()

            time.sleep(1)  # set length of simulation period (5s)

            # turn off all stimuli and prepare for next trial
            for x in range(12):
                stim[x].toggleOff()

        time.sleep(1)  # x second break between trials (120s)

    print("all trials finished")
    f.write("Session finished.\n\n")
    f.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = QWidget()
    demo.setWindowTitle('Flashing Stim 1')

    layout = QGridLayout()

    demo.setStyleSheet("background-color: black;")
    titleLabel = QLabel(
        '<h1 style="text-align:center; color: white">ODC-DEMO</h1>')
    layout.addWidget(titleLabel, 0, 0, 1, 4)

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

    for row in range(3):
        for col in range(4):
            stimNum = row*4+col
            stim[stimNum].toggleOff()
            layout.addWidget(stim[stimNum], row+1, col)

    demo.setLayout(layout)
    demo.resize(500, 500)
    demo.show()

    stopThread = False
    x = threading.Thread(target=thread_function, args=(lambda: stopThread,))
    x.start()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        stopThread = True
        print('Closing Window...')
