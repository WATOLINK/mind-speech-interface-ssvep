from PyQt5 import QtWidgets
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
        self.yesButton = ButtonContainer("Yes")
        self.noButton = ButtonContainer("No")

        topLayout.addWidget(self.yesButton)
        topLayout.addWidget(self.noButton)

        self.dummyWidget = QtWidgets.QWidget()
        self.dummyWidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        bottomLayout.addWidget(self.dummyWidget) # Dummy widget
        bottomLayout.addWidget(confirmButton)
        bottomLayout.addWidget(self.dummyWidget) # Dummy widget

        self.dummyButton = QtWidgets.QPushButton()
        self.dummyButton.setCheckable(True)
        self.buttonGroup = QtWidgets.QButtonGroup()
        self.buttonGroup.addButton(self.yesButton)
        self.buttonGroup.addButton(self.noButton)
        self.buttonGroup.addButton(self.dummyButton)
        
        self.generalLayout.addLayout(topLayout)
        self.generalLayout.addLayout(bottomLayout)

        self.generalLayout.setStretch(0, 3)
        self.generalLayout.setStretch(1, 1)
        
        # self.confirm_button = QtWidgets.QPushButton('Confirm')
        # self.confirm_button.setStyleSheet(confirmButtonStyle)
        # layout.addWidget(self.confirm_button, 2, 1)
        confirmButton.clicked.connect(self.confirm_clicked)

        self.setLayout(self.generalLayout)


        #automated selection part
        value = signalReceived()
        self.automatedSelection(value)

    # Following functions are called when a yes, no, or confirm stimuli is detected by event loop (not implemented yet)

    def confirm_clicked(self):
        if (self.yesButton.isChecked() == True):
            self.dummyButton.setChecked(True)
            # Do what we want when yes is checked and confirm is clicked
        elif (self.noButton.isChecked() == True):
            self.dummyButton.setChecked(True)
            # Do what we want when no is checked and confirm is clicked

    def automatedSelection(self, value):
        if value == 111111:
            self.yesButton.setChecked(True)
        elif value == 222222:
            self.noButton.setChecked(True)

#run this code when the signal is received with the 6 digit value
def signalReceived():
    receivedValue = 222222      #temporarily hardcoded values, will be replaced with the API call
    return receivedValue
