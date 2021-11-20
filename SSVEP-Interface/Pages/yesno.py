import functools
from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont
from qtwidgets import AnimatedToggle


class YesNoWindow(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        yes_toggle = AnimatedToggle(
            checked_color="#03a9fc",
            pulse_checked_color="#4403a9fc"
        )

        no_toggle = AnimatedToggle(
            checked_color="#03a9fc",
            pulse_checked_color="#4403a9fc"
        )

        layout = QtWidgets.QGridLayout()

        yes_label = QtWidgets.QLabel('Yes')
        yes_label.setFont(QFont('Helvetica', 24))
        layout.addWidget(yes_label, 0, 0)
        layout.addWidget(yes_toggle, 0, 1)

        no_label = QtWidgets.QLabel('No')
        no_label.setFont(QFont('Helvetica', 24))
        layout.addWidget(no_label, 1, 0)
        layout.addWidget(no_toggle, 1, 1)

        yes_toggle.stateChanged.connect(functools.partial(self.yesToggleOn, yes_toggle, no_toggle))
        no_toggle.stateChanged.connect(functools.partial(self.noToggleOn, yes_toggle, no_toggle))

        confirm_button = QtWidgets.QPushButton('Confirm')
        confirm_button.setFont(QFont('Helvetica'))
        layout.addWidget(confirm_button, 2, 1)

        self.setLayout(layout)

    def yesToggleOn(self, yes_toggle, no_toggle):
        if yes_toggle.isChecked():
            no_toggle.setCheckState(False)

    def noToggleOn(self, yes_toggle, no_toggle):
        if no_toggle.isChecked():
            yes_toggle.setCheckState(False)
