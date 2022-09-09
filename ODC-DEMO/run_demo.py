from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QWidget,
    QVBoxLayout
)
import sys
import threading
import datetime
from configs import HOR, VERT
from multi_stim_demo import *


if __name__ == '__main__':
    distance = int(input("Distance between stimuli:\n"))
    radius = input("Radius of stimuli (0.5 default):\n")

    if radius == None or not radius:
        radius = 0.5
    else:
        radius = float(radius)

    # File and GUI config
    x = datetime.datetime.now()

    # day of year, year, millisecond
    filename = f"{x.strftime('%j')}_{x.strftime('%Y')}_{x.strftime('%f')}"

    file = open("demo_data/" + filename + ".txt", "x")  # create log

    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle('Flashing Stim 1')
    window.setStyleSheet("background-color: black;")

    layout = QVBoxLayout()

    # global label
    label = QLabel(labelTxt("ODC-DEMO"))
    label.setFixedHeight(100)
    layout.addWidget(label)
    grid = Stimuli(distance, radius)  # stimuli grid widget

    layout.addWidget(grid)
    window.setLayout(layout)

    # BCI Config
    board_details = Cyton_Board_Config(False)

    stopThread = False
    x = threading.Thread(target=display_procedure, args=(
        lambda: stopThread, board_details[0], board_details[1], label, filename))
    x.start()

    window.setFixedSize(HOR, VERT)  # initial window size
    window.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        file.close()
        print('Closing Window...')
        stopThread = True # terminate process

    x.join() # kill thread
    print('Thread Killed')