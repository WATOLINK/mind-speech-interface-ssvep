from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from Pages.styles import toggleButtonStyle, yesLabelStyle, toggleButtonStyleNoBorder
from Pages.circle_stimuli import CircleFlash

class ButtonContainer(QtWidgets.QPushButton):
    def __init__(self, labelText="", freq=60, red=255, green=255, blue=255, horizontal=False, parent=None, checkable=True, border=True):
        super(ButtonContainer, self).__init__(parent)
        self.setMinimumHeight(150)
        if border:
            self.setStyleSheet(toggleButtonStyle)
        else:
            self.setStyleSheet(toggleButtonStyleNoBorder)
        self.setCheckable(checkable)

        if horizontal:
            self.layout = QtWidgets.QHBoxLayout()
        else:
            self.layout = QtWidgets.QVBoxLayout()

        self.layout.setContentsMargins(25, 25, 25, 25)
        
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        # Configure label
        self.setLayout(self.layout)
        self.label = QtWidgets.QLabel(labelText)
        self.label.setStyleSheet(yesLabelStyle)
        self.label.setAlignment(Qt.AlignCenter)

        # Add label
        self.layout.addWidget(self.label)

        # Configure stimuli
        self.stimuli = CircleFlash(freq, red, green, blue)
        self.stimuli.setMinimumHeight(400)
        self.stimuli.setMinimumWidth(400)
        self.stimuli.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        # Add stimuli
        self.layout.addWidget(self.stimuli, alignment=Qt.AlignCenter)


        self.layout.setStretch(0, 2)
        self.layout.setStretch(1, 1)

    def setLabelText(self, text):
        self.label.setText(text)

    def labelText(self):
        return self.label.text()

    



    
        