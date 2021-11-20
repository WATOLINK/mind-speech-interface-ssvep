import sys

from PyQt5.QtWidgets import QApplication, QPushButton, QTextEdit, QVBoxLayout, QWidget, QLineEdit, QRadioButton
from PyQt5 import QtCore, QtGui

#Function that is being executed by external commands
def nuts():
    textBox.insertPlainText("nuts ")

#Check if the text in the textbox is desired
def checkdeez():
    s = lineText.text()
    if (s=='deez'):
        #Connected to function 'nuts'
        nuts()
        lineText.clear()

#Moves the mouse position to the desired widget
def moveMouse():
    p = QtCore.QPoint(window.pos()+lineText.pos())
    p.setX(p.x()+10)
    p.setY(p.y()+10)
    
    QtGui.QCursor.setPos(p)

#Initialize window
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('Multiple Input Sockets Example')
layout = QVBoxLayout()

#Initialize widgets
textBox = QTextEdit('', parent = window)
deezbtn = QPushButton('deez', parent=window)
lineText = QLineEdit('', parent=window)
radioBtn = QRadioButton('deez', parent=window)
mouseBtn = QPushButton('Move Mouse', parent=window)

#Method 1: Connect commands with desired output, in this case it would be the function 'nuts'
deezbtn.clicked.connect(nuts)
lineText.returnPressed.connect(checkdeez)   #Function 'checkdeez' is internally connected to function 'nuts'
radioBtn.clicked.connect(nuts)

#Method 2: Move mouse to a button, when clicked runs desired output
mouseBtn.clicked.connect(moveMouse)


layout.addWidget(textBox)
layout.addWidget(deezbtn)
layout.addWidget(lineText)
layout.addWidget(radioBtn)
layout.addWidget(mouseBtn)

window.setLayout(layout)
window.show()
sys.exit(app.exec())