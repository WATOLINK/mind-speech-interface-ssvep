from PyQt5.QtWidgets import (
    QLabel,
    QWidget,
    QGridLayout,
    QHBoxLayout,
    QFrame,
)
from PyQt5.QtCore import QRect, Qt
from time import time, sleep
from brainflow.board_shim import BoardShim, BrainFlowInputParams
import random
import datetime
import circle_stimuli as Stim
import numpy as np
import pandas as pd
import argparse
from configs import *

color_code_order = []
color_freq_order = []

def display_procedure(stop, board, args, label, filename):
    START_DELAY_S, NUM_TRIALS, INDICATOR_TIME_VALUE_S, TRIAL_BREAK_TIME, STIM_TIME = demo_configs()

    f = open("demo_data/" + filename +
             ".txt", 'a')  # modify depending on CWD
    f.write(f"Session at {datetime.datetime.now()} \n\n")
    start_time = time()
    board.start_stream(450000, args)
    sleep(1)
    startDelay = START_DELAY_S
    for x in range(startDelay):
        label.setText(labelTxt(f"Starting in {str(startDelay-x)}"))
        sleep(1)

    # NUM_STIMS == STIM_PERIOD_TRAILS are the same
    order = list(range(NUM_STIMS))

    for trial in range(NUM_TRIALS):  # number of trials (5 times)
        print("=====Trial "+str(trial+1)+"=====")
        f.write("\n=====Trial "+str(trial+1)+"=====\n")

        # each trial will have a different order of stimulus
        random.shuffle(order)
        print(order)

        color_code_order.append(0)
        color_freq_order.append(0)
        # insert marker for start AS WELL AS BETWEEN TRIALS
        board.insert_marker(0.666)

        for stimPeriod in range(NUM_STIMS):
            color_code_order.append(0)
            color_freq_order.append(0)
            # just for testing otherwise the thread keeps running if you close the window
            if stop():
                break
            currentStim = stim[order[stimPeriod]]
            stimLabel = preStimIndicators[order[stimPeriod]]

            # log color and hz to terminal
            color = str(currentStim.rValue) + "," + \
                str(currentStim.gValue) + "," + str(currentStim.bValue)
            colorCode = ""
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
            # insert marker for in between flashes (null)
            board.insert_marker(0.666)

            for x in range(NUM_STIMS):
                stim[x].toggleOn()
            sleep(STIM_TIME)  # set length of simulation period (5s)
            # insert marker for stimuli flash (individual)
            board.insert_marker(0.666)

            # turn off all stimuli and prepare for next trial
            for x in range(NUM_STIMS):
                stim[x].toggleOff()

        # just for testing otherwise the thread keeps running if you close the window
        if stop():
            break

        # trial break
        for x in range(int(TRIAL_BREAK_TIME)):
            label.setText(
                labelTxt(f"Time before next trial: ({TRIAL_BREAK_TIME-x})"))
            sleep(1)

    color_code_order.append(0)
    color_freq_order.append(0)
    data = board.get_board_data().transpose()

    label.setText(
        labelTxt(f"Trials finished"))
    print("all trials finished")
    f.write("Session finished.\n\n")
    f.close()

    board.stop_stream()
    if not TESTING:
        duration = time()-start_time
        generate_test_report(board, duration, data,
                             color_code_order, color_freq_order)
    df = post_process(data, start_time, color_code_order,
                      color_freq_order, board.board_id)
    try:
        if TESTING:
            df.to_csv("ODC-DEMO/test.csv", index=False)
        else:
            df.to_csv("ODC-DEMO/demo_data/" + filename + ".csv", index=False)
    except:
        print('Post data processing and CSV Export failed')
    finally:
        Cyton_Board_End(board)

def labelTxt(text):
    return f'<h1 style="text-align:center; color: white">{text}</h1>'

def post_process(data, start_time, color_code, color_freq, boardId):
    split_indices = np.where(data == 0.666)[0]

    # OpenBCI
    if boardId == 0:
        unix_timestamp = data[:, 22:23]
        data = np.delete(data, 0, 1)
        data = np.delete(data, range(8, 23), 1)
    # Virtual Board
    elif boardId == -1:
        unix_timestamp = data[:, 30:31]
        data = np.delete(data, 0, 1)
        data = np.delete(data, range(8, 31), 1)
    # GTech Unicorn
    else:
        unix_timestamp = data[:, 17:18]
        data = np.delete(data, range(8, 19), 1)
    main_timestamp = []
    
    for i in range(len(unix_timestamp)):
        main_timestamp.append(
            datetime.datetime.fromtimestamp(unix_timestamp[i][0]))

    main_timestamp = np.array(main_timestamp).reshape(-1, 1)
    data = np.concatenate((main_timestamp, data), axis=1)
    data = np.split(data, split_indices)

    # Create header row
    header = []
    header.append("time")
    for i in range(1, 9):
        header.append('CH{}'.format(i))

    # Convert data blocks from NumPy arrays to pandas DataFrames
    for i in range(len(data)):
        data[i] = pd.DataFrame(data[i], columns=header)

    # Put color code and frequency columns together with data blocks
    for data_block, code, freq in zip(data, color_code, color_freq):
        data_block.loc[0, 'Color Code'] = code
        data_block.loc[0, 'Frequency'] = freq

    # Combine to 1 DataFrame
    for i in range(len(data)):
        data[i] = data[i].to_numpy()

    for i in range(0, len(data)-1):
        data[i+1] = np.concatenate((data[i], data[i+1]), axis=0)

    df_data = data[-1]
    header.append('Color Code')
    header.append('Frequency')
    df_all = pd.DataFrame(df_data, columns=header)
    return df_all

def generate_test_report(board, duration, data, color_code_order, color_freq_order):
    tf = open("ODC-DEMO/test_report.txt", 'w')
    tf.write("Size of Data List: ")
    tf.write(str(np.shape(data)))
    tf.write("\n")
    tf.write("Size of Color Code List: ")
    tf.write(str(len(color_code_order)))
    tf.write("\n")
    tf.write("Size of Color Freq List: ")
    tf.write(str(len(color_freq_order)))
    tf.write("\n\n")
    tf.write("Channel Names: ")
    for i in board.get_eeg_names(0):
        tf.write(i)
        tf.write(", ")
    tf.write("\n\n")
    tf.write("Channel Numbers: ")
    for i in board.get_eeg_channels(0):
        tf.write(str(i))
        tf.write(", ")
    tf.write("\n\n")
    tf.write("Number of Channels: ")
    tf.write(str(board.get_num_rows(0)))
    tf.write("\n\n")
    tf.write("Marker Channel: ")
    tf.write(str(board.get_marker_channel(0)))
    tf.write("\n")
    tf.write("Data Acquisition Duration: ")
    tf.write(str(duration))
    tf.write("\n\n")
    tf.write("Expected Samples: ")
    tf.write(str(board.get_sampling_rate(0)*duration))
    tf.write("\n")
    tf.write("Received Samples: ")
    tf.write(str(np.shape(data)[0]))
    tf.write("\n")
    tf.close()

def Cyton_Board_Config(purpose):

    BoardShim.enable_dev_board_logger()

    parser = argparse.ArgumentParser()
    # use docs to check which parameters are required for specific board, e.g. for Cyton - set serial port
    parser.add_argument('--timeout', type=int,
                        help='timeout for device discovery or connection', required=False, default=0)
    parser.add_argument('--ip-port', type=int,
                        help='ip port', required=False, default=0)
    parser.add_argument('--ip-protocol', type=int,
                        help='ip protocol, check IpProtocolType enum', required=False, default=0)
    parser.add_argument('--ip-address', type=str,
                        help='ip address', required=False, default='')
    parser.add_argument('--serial-port', type=str,
                        help='serial port', required=False, default='')
    parser.add_argument('--mac-address', type=str,
                        help='mac address', required=False, default='')
    parser.add_argument('--other-info', type=str,
                        help='other info', required=False, default='')
    parser.add_argument('--streamer-params', type=str,
                        help='streamer params', required=False, default='')
    parser.add_argument('--serial-number', type=str,
                        help='serial number', required=False, default='')
    parser.add_argument('--board-id', type=int,
                        help='board id, check docs to get a list of supported boards', required=False)
    parser.add_argument('--file', type=str, help='file',
                        required=False, default='')
    args = parser.parse_args()

    params = BrainFlowInputParams()
    params.ip_port = args.ip_port
    params.serial_port = args.serial_port
    params.mac_address = args.mac_address
    params.other_info = args.other_info
    params.serial_number = args.serial_number
    params.ip_address = args.ip_address
    params.ip_protocol = args.ip_protocol
    params.timeout = args.timeout
    params.file = args.file

    # Cyton Board Object
    board = BoardShim(args.board_id, params)

    # Start Acquisition
    board.prepare_session()

    # For entire program
    if purpose:
        board.start_stream(45000, args.streamer_params)
        return board
    # For Demo
    else:
        return [board, args.streamer_params]

def Cyton_Board_End(board):
    board.release_session()
    return

class Stimuli(QWidget):
    def __init__(self, numOStims, arrOFreq, arrORad, distance=1):
        super().__init__()
        self.resize(1800, 1300)

        # ensures correct aspect ratio of grid
        self.frame = QFrame(self, objectName="frame")
        global stim
        stim = []  # number of stimulus

        # stimuli expectations
        assert numOStims % 2 == 0, "number of stimuli should be 4, 6, or 8"
        assert 4 <= numOStims and numOStims <= 8, "number of stimuli should be 4, 6, or 8"
        assert numOStims == len(arrOFreq), "frequencies given should match number of stimuli"
        assert numOStims == len(arrORad), "radii given should match number of stimuli"

        # white stims
        for i in range(numOStims):
            stim.append(Stim.CircleFlash(arrOFreq[i], 255, 255, 255, i+1, arrORad[i]))

        # append stimulis to grid in random order
        random.shuffle(stim)

        # create array of indicators
        global preStimIndicators
        preStimIndicators = []

        # labels above stimulus before
        for _ in range(len(stim)):
            preStim = QLabel(labelTxt(""))
            preStimIndicators.append(preStim)
        self.gridLayout = QGridLayout(self.frame)

        # this iteration will be performed for 4, 6 stimuli
        if numOStims != 8:
            stimNum = 0
            for row in range(2): # numOStims / (numOStims//2)
                for col in range(numOStims//2):
                    stim[stimNum].toggleOff()
                    self.gridLayout.addWidget(stim[stimNum], row, col)
                    stimNum += 1
        else: # 8 stimuli : we want different format
            for stimNum in range(numOStims):
                stim[stimNum].toggleOff()

            self.gridLayout.addWidget(stim[0], 0, 3)
            self.gridLayout.addWidget(stim[1], 1, 0)
            self.gridLayout.addWidget(stim[2], 1, 1)
            self.gridLayout.addWidget(stim[3], 1, 2)
            self.gridLayout.addWidget(stim[4], 1, 3)

            bottomGrid = QHBoxLayout()
            bottomGrid.addWidget(stim[5])
            bottomGrid.addWidget(stim[6])
            bottomGrid.addWidget(stim[7])
            self.gridLayout.addLayout(bottomGrid, 2, 0, 1, 4)

        self.gridLayout.setSpacing(distance)

    # resizes grid during window resize
    def resizeEvent(self, event):
        super().resizeEvent(event)

        l = min(self.width(), self.height())
        center = self.rect().center()

        rect = QRect(0, 0, int(l*(14/9)), l)  # 5 x 3 ratio
        rect.moveCenter(center)
        self.frame.setGeometry(rect)