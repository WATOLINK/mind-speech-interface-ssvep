import sys
from PyQt5.QtWidgets import QApplication, QButtonGroup, QWidget, QGridLayout, QLineEdit, QLabel, QPushButton, QStackedWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore

from Pages.styles import textBoxStyle, sideBarStyle, mainButtonStyle, promptBoxStyle, instructionsStyle
from Pages.button_container import ButtonContainer
from Pages.MCPage.mc2 import MultipleChoiceWidget
from Pages.YNPage.yesno2 import YesNoWidget
from Pages.QAPage.keyboard2 import KeyboardWidget
from Pages.HelpPage.help import HelpWidget
from Pages.sidebar.sidebar import Sidebar


class HomePageWidget(QWidget):
    def __init__(self, parent):
        super().__init__()

        layout = QGridLayout()
        self.setLayout(layout)

        width = 4
        height = 6
        mainWidget = mainStack(self)
        
        layout.addWidget(title(), 0, 0, 1, 1)
        layout.addWidget(promptBox(), 1, 0, 1, 3)
        layout.addWidget(inputBox(), 2, 0, 1, 3)
        layout.addWidget(mainWidget, 3, 0, 4, 3)
        layout.addWidget(Sidebar(self), 1, 4, height, 1)

        self.initUI()

    def initUI(self):

        self.setGeometry(100, 100, 900, 900)
        self.setWindowTitle('Icon')
        self.setWindowIcon(QIcon('web.png'))

        self.show()


def title():
    global title
    title = QLabel("test")
    title.setMaximumHeight(40)
    return title


def promptBox():
    prompt = QLabel("AMONG US")
    prompt.setStyleSheet(promptBoxStyle)
    prompt.setAlignment(QtCore.Qt.AlignCenter)
    prompt.setObjectName("Prompt")
    return prompt


def inputBox():
    textbox = QLineEdit()
    textbox.setStyleSheet(textBoxStyle)
    textbox.setObjectName("Input")
    return textbox


def mainStack(parent):
    stack = QStackedWidget()
    stack.setObjectName("Main Stack")
    stack.setStyleSheet(mainButtonStyle)

    stack.addWidget(homeWidget(parent))  # 0
    stack.addWidget(MultipleChoiceWidget(parent))  # 1
    stack.addWidget(YesNoWidget(parent))  # 2
    stack.addWidget(KeyboardWidget(parent))  # 3
    stack.addWidget(HelpWidget(parent))  # 4

    return stack


def homeWidget(parent):
    home = QWidget()
    layout = QHBoxLayout()

    labels = ['MC', 'YN', 'Type']
    buttons = []

    for label in labels:
        button = ButtonContainer(label) 
        button.setObjectName(label)
        buttons.append(button)
        layout.addWidget(button)

    buttons[0].clicked.connect(
        lambda: disableOtherButtons(buttons, buttons[0]))
    buttons[1].clicked.connect(
        lambda: disableOtherButtons(buttons, buttons[1]))
    buttons[2].clicked.connect(
        lambda: disableOtherButtons(buttons, buttons[2]))

    home.setLayout(layout)
    return home

def disableOtherButtons(buttons, selected):
    
    if selected.isChecked():
        title.setText(selected.label.text())
        for button in buttons:
            if button != selected:
                button.setChecked(False)
    else:
        title.setText("")
