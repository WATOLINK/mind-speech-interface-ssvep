import functools
from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont
from qtwidgets import AnimatedToggle
from Pages.stimuli import Flash

class YesNoWindow(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        
        yes_toggle = QtWidgets.QPushButton("Yes")
        yes_toggle.setCheckable(True)
        # yes_toggle.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        no_toggle = QtWidgets.QPushButton("No")
        no_toggle.setCheckable(True)
        # no_toggle.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.buttonGroup = QtWidgets.QButtonGroup()
        self.buttonGroup.addButton(yes_toggle)
        self.buttonGroup.addButton(no_toggle)

        layout = QtWidgets.QGridLayout()

        layout.addWidget(yes_toggle, 0, 0)
        layout.addWidget(no_toggle, 0, 1)
        
        #add stims
        w1 = Flash(400,0,0,255,1)
        w2 = Flash(50,255,0,0,1)
        layout.addWidget(w1, 1, 0)
        layout.addWidget(w2, 1, 1)

        confirm_button = QtWidgets.QPushButton('Confirm')
        confirm_button.setFont(QFont('Helvetica'))
        layout.addWidget(confirm_button, 2, 1)

        self.setLayout(layout)
