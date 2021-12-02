import functools
from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont
from Pages.stimuli import Flash


class YesNoWindow(QtWidgets.QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        # This button is not shown to the user, only exists so that the yes/no buttons can be deselected
        self.default_toggle = QtWidgets.QPushButton("")
        self.default_toggle.setCheckable(True)

        self.yes_toggle = QtWidgets.QPushButton("Yes")
        self.yes_toggle.setCheckable(True)
        # yes_toggle.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.no_toggle = QtWidgets.QPushButton("No")
        self.no_toggle.setCheckable(True)
        # no_toggle.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.buttonGroup = QtWidgets.QButtonGroup()
        self.buttonGroup.addButton(self.yes_toggle)
        self.buttonGroup.addButton(self.no_toggle)
        self.buttonGroup.addButton(self.default_toggle)

        layout = QtWidgets.QGridLayout()

        layout.addWidget(self.yes_toggle, 0, 0)
        layout.addWidget(self.no_toggle, 0, 1)

        # Buttons used to test stimuli detect functions

        # self.y = QtWidgets.QPushButton("y")
        # self.n = QtWidgets.QPushButton("n")
        # self.y.clicked.connect(self.yes_detect)
        # self.n.clicked.connect(self.no_detect)
        # layout.addWidget(self.y, 2, 0)
        # layout.addWidget(self.n, 2, 2)

        # add stims
        w1 = Flash(400, 0, 0, 255, 1)
        w2 = Flash(50, 255, 0, 0, 1)
        layout.addWidget(w1, 1, 0)
        layout.addWidget(w2, 1, 1)

        self.confirm_button = QtWidgets.QPushButton('Confirm')
        self.confirm_button.setFont(QFont('Helvetica'))
        layout.addWidget(self.confirm_button, 2, 1)
        self.confirm_button.clicked.connect(self.confirm_detect)

        self.setLayout(layout)

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
