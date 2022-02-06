from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from Pages.circle_stimuli import CircleFlash
from Pages.styles import confirmButtonStyle, stimuliStyle, toggleButtonStyle, yesLabelStyle
from Pages.stimuli import Flash
from Pages.button_container import ButtonContainer


class YesNoWindow(QtWidgets.QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        self.generalLayout = QtWidgets.QVBoxLayout()


        topLayout = QtWidgets.QHBoxLayout()
    

        bottomLayout = QtWidgets.QHBoxLayout()
        bottomLayout.setStretch(0, 1)
        bottomLayout.setStretch(1, 1)
        bottomLayout.setStretch(2, 1)
        
        confirmButton = ButtonContainer("Confirm", horizontal=True, checkable=False, border=False)
        yesButton = ButtonContainer("Yes")
        noButton = ButtonContainer("No")

        topLayout.addWidget(yesButton)
        topLayout.addWidget(noButton)

        dummyWidget = QtWidgets.QWidget()
        dummyWidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        bottomLayout.addWidget(dummyWidget) # Dummy widget
        bottomLayout.addWidget(confirmButton)
        bottomLayout.addWidget(dummyWidget) # Dummy widget
        
        self.generalLayout.addLayout(topLayout)
        self.generalLayout.addLayout(bottomLayout)


        self.generalLayout.setStretch(0, 3)
        self.generalLayout.setStretch(1, 1)
        


        # self.confirm_button = QtWidgets.QPushButton('Confirm')
        # self.confirm_button.setStyleSheet(confirmButtonStyle)
        # layout.addWidget(self.confirm_button, 2, 1)
        # self.confirm_button.clicked.connect(self.confirm_detect)

        self.setLayout(self.generalLayout)

    # Following functions are called when a yes, no, or confirm stimuli is detected by event loop (not implemented yet)

    def yes_detect(self):
        self.yes_toggle.setChecked(True)

    def no_detect(self):
        self.no_toggle.setChecked(True)

    def confirm_detect(self):
        y_check = self.yes_toggle.isChecked()
        n_check = self.no_toggle.isChecked()
        if (y_check == True):
            self.default_toggle.setChecked(True)
            # Do what we want when yes is checked and confirm is clicked

        elif (n_check == True):
            self.default_toggle.setChecked(True)
            # Do what we want when no is checked and confirm is clicked
