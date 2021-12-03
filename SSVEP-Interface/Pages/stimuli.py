import sys

# https://doc.qt.io/qt-6/qopenglwidget.html

# 1. Import `QApplication` and all the required widgets
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QWidget,
    QGridLayout,
    QOpenGLWidget,
)
from PyQt5.QtCore import (
    Qt,
    QTimer
)
from PyQt5.QtGui import (
    QOpenGLVersionProfile,
)
import random


class Flash (QOpenGLWidget):
    rValue = 0
    gValue = 0
    bValue = 0
    opacityValue = 0

    def __init__(self, freq, r, g, b, opacity):
        super() . __init__()
        self.flag = True

        self.rValue = r/255
        self.gValue = g/255
        self.bValue = b/255
        opactiyValue = opacity

        # using Qt.PreciseTimer, which is accurate to 1ms
        timer = QTimer(self, interval=freq, timerType=0)
        # calls paintGL/ updates widget
        timer.timeout.connect(lambda: self.update())
        timer.start()

    def initializeGL(self):
        # set up GL
        version_profile = QOpenGLVersionProfile()
        version_profile.setVersion(2, 0)
        self.gl = self.context().versionFunctions(version_profile)
        self.gl.initializeOpenGLFunctions()

        # set initial colors
        self.gl.glClearColor(self.rValue, self.gValue,
                             self.bValue, self.opacityValue)
        # depth testing
        self.gl.glEnable(self.gl.GL_DEPTH_TEST)

    def paintGL(self):
        # print("updating")
        if self.flag:
            self.gl.glClearColor(0, 0, 0, 1) # black

            # print("clear")
        else:
            self.gl.glClearColor(self.rValue, self.gValue, self.bValue, self.opacityValue)
            # print("set")
        self.flag = not self.flag


# for testing, doesnt actually do stuff when you run main
if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = QWidget()
    demo.setWindowTitle('Flashing Stim 1')

    layout = QGridLayout()

    titleLabel = QLabel(
        '<h1 style="text-align:center">Flashing Stimuli 1</h1>')
    layout.addWidget(titleLabel, 0, 0, 2, 6)

    w1 = Flash(400, random.randrange(1, 255), random.randrange(
        1, 255), random.randrange(1, 255), 1)
    w1.setAttribute(Qt.WA_StyledBackground, True)

    w2 = Flash(400, random.randrange(1, 255), random.randrange(
        1, 255), random.randrange(1, 255), 1)
    w2.setAttribute(Qt.WA_StyledBackground, True)

    w3 = Flash(200, random.randrange(1, 255), random.randrange(
        1, 255), random.randrange(1, 255), 1)
    w3.setAttribute(Qt.WA_StyledBackground, True)

    w4 = Flash(200, random.randrange(1, 255), random.randrange(
        1, 255), random.randrange(1, 255), 1)
    w4.setAttribute(Qt.WA_StyledBackground, True)

    w5 = Flash(100, random.randrange(1, 255), random.randrange(
        1, 255), random.randrange(1, 255), 1)
    w5.setAttribute(Qt.WA_StyledBackground, True)

    w6 = Flash(100, random.randrange(1, 255), random.randrange(
        1, 255), random.randrange(1, 255), random.randrange(1, 255))
    w6.setAttribute(Qt.WA_StyledBackground, True)

    layout.addWidget(w1, 2, 0)
    layout.addWidget(w2, 2, 1)
    layout.addWidget(w3, 2, 2)
    layout.addWidget(w4, 2, 3)
    layout.addWidget(w5, 2, 4)
    layout.addWidget(w6, 2, 5)

    demo.setLayout(layout)
    demo.resize(500, 500)
    demo.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')
