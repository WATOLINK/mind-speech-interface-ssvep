import sys
from math import cos, sin, pi

# https://doc.qt.io/qt-6/qopenglwidget.html 

# 1. Import `QApplication` and all the required widgets
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QWidget,
    QGridLayout,
    QHBoxLayout,
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


class CircleFlash (QOpenGLWidget):
    rValue = 0
    gValue = 0
    bValue = 0
    opacityValue = 0

    def __init__(self,freq, r, g, b,opacity):
        super() . __init__()
        self.flag = True

        self.rValue = r/255
        self.gValue = g/255
        self.bValue = b/255
        opactiyValue = opacity

        timer = QTimer(self, interval=freq, timerType = 0)  # using Qt.PreciseTimer, which is accurate to 1ms
        timer.timeout.connect(lambda: self.update()) # calls paintGL/ updates widget
        timer.start()

    def initializeGL(self):
        # set up GL
        version_profile  = QOpenGLVersionProfile() 
        version_profile.setVersion(2,0)
        self.gl = self.context().versionFunctions(version_profile)
        self.gl.initializeOpenGLFunctions()

        # depth testing 
        self.gl.glEnable(self.gl.GL_DEPTH_TEST)

    def paintGL(self):
        if self.flag:  
            # increase sides to get smoother edges
            sides = 64    

            # radius decides the percentage of the widget the circle occupies
            radius = 1   

            # set circle colour
            self.gl.glColor3f(self.rValue, self.gValue, self.bValue);

            # start drawing circle
            self.gl.glBegin(self.gl.GL_TRIANGLE_FAN)    
            for i in range(sides):    
                x = radius * cos(i * 2 * pi / sides)
                y = radius * sin(i * 2 * pi / sides)
                self.gl.glVertex2f(x, y)
            self.gl.glEnd()    

        self.flag = not self.flag

# for testing, doesnt actually do stuff when you run main
if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = QWidget()
    demo.setWindowTitle('Flashing Stim 1')

    layout = QHBoxLayout()

    w1 = CircleFlash(400,random.randrange(1,255), random.randrange(1,255), random.randrange(1,255), 1)

    layout.addWidget(w1)


    demo.setLayout(layout)
    demo.resize(500, 500)
    demo.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')
