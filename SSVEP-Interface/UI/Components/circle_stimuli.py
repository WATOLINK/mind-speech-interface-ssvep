import sys
from math import cos, sin, pi
import time

# https://doc.qt.io/qt-6/qopenglwidget.html 

# 1. Import `QApplication` and all the required widgets
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QHBoxLayout,
    QOpenGLWidget,
    QSizePolicy
)
from PyQt5.QtCore import QTimer, Qt

from PyQt5.QtGui import QOpenGLVersionProfile



class CircleFlash (QOpenGLWidget):
    rValue = 0
    gValue = 0
    bValue = 0
    on = True

    def __init__(self,freqHz, r, g, b):
        super() . __init__()
        self.flag = True

        self.rValue = r
        self.gValue = g
        self.bValue = b
        self.freqHertz = freqHz
        self.setAttribute(Qt.WA_AlwaysStackOnTop)

        timer = QTimer(self, interval=(1000/(freqHz*2)), timerType = 0)  # using Qt.PreciseTimer, which is accurate to 1ms
        #freq is x2 since the freq needed is by # of times on, instead of times changed between on and 
        timer.timeout.connect(lambda: self.update()) # calls paintGL/ updates widget
        timer.start()

    def initializeGL(self):
        # set up GL
        version_profile  = QOpenGLVersionProfile() 
        version_profile.setVersion(2,0)
        
        self.gl = self.context().versionFunctions(version_profile)
        
        self.gl.initializeOpenGLFunctions()
        self.gl.glClearColor(0.0, 0.0, 0.0, 0.0)

        # depth testing 
        self.gl.glEnable(self.gl.GL_DEPTH_TEST)

    def paintGL(self):
        if self.on:
            if self.flag:  
                # increase sides to get smoother edges
                sides = 64    

                # radius decides the percentage of the widget the circle occupies
                radius = 1

                # set circle colour
                self.gl.glColor3f(self.rValue/255, self.gValue/255, self.bValue/255);

                # start drawing circle
                self.gl.glBegin(self.gl.GL_TRIANGLE_FAN)    
                for i in range(sides):    
                    x = radius * cos(i * 2 * pi / sides)
                    y = radius * sin(i * 2 * pi / sides)
                    self.gl.glVertex2f(x, y)
                self.gl.glEnd()    

            self.flag = not self.flag
        else:
            self.gl.glClearColor(0.0, 0.0, 0.0, 0.0)
    
    def toggleOn(self): 
        self.on = True
        
    def toggleOff(self):
        self.on = False

# for testing, doesnt actually do stuff when you run main
if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = QWidget()
    demo.setWindowTitle('Flashing Stim 1')

    layout = QHBoxLayout()

    w1 = CircleFlash(4,255,255,255)

    layout.addWidget(w1)


    demo.setLayout(layout)
    demo.resize(500, 500)
    demo.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')
