from PyQt5.QtWidgets import QApplication, QButtonGroup, QWidget, QGridLayout, QLineEdit, QLabel, QPushButton, QStackedWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore

from UI.styles import textBoxStyle, sideBarStyle, mainButtonStyle, promptBoxStyle, instructionsStyle
from UI.Components.button_container import ButtonContainer
from UI.KeyboardPage.keyboard2 import KeyboardWidget
from UI.HelpPage.help import HelpWidget
from UI.BottomWidget.bottomWidget import BottomWidget
from UI.KeyboardPage.completer2 import suggestWords

from UI.Components.enterButton import EnterButton

from UI.UI_DEFS import getMainWidgetIndex, MainWidgetIndexes
from UI.BottomWidget.bottomWidgetIndexes import getBottomIndex

from UI.status import setOutputMode, setCurrentPage, printStatus

from UI.helperFunctions import disableOtherButtons, changeStacks


def OutputModeWidget(parent):
    outputMode = QWidget()
    layout = QVBoxLayout()
    outputMode.setObjectName("output menu")
    layout.addWidget(OutputModeUpper(parent))
    layout.addWidget(OutputModeLower(parent))
    outputMode.setLayout(layout)
    return outputMode


def OutputModeUpper(parent):
    outputMode = QWidget()
    layout = QHBoxLayout()
    outputMode.setObjectName("Output Menu")

    labels = ['Twitter','Voice','Visual Communication']
    buttons = []

    for label in range(len(labels)):
        button = ButtonContainer(labels[label])
        button.setObjectName(labels[label])
        layout.addWidget(button)
        buttons.append(button)

    buttons[0].clicked.connect(
        lambda: disableOtherButtons(buttons, buttons[0]))
    buttons[1].clicked.connect(
        lambda: disableOtherButtons(buttons, buttons[1]))
    buttons[2].clicked.connect(
        lambda: disableOtherButtons(buttons, buttons[2]))

    outputMode.setLayout(layout)
    return outputMode

def OutputModeLower(parent):
    sidebar = QWidget()
    layout = QHBoxLayout()

    buttons = []

    # buttons.append(EnterButton(parent))
    buttons.append(ButtonContainer("Help",checkable=False))
    
    for button in buttons:
        layout.addWidget(button)

    # buttons[0].clicked.connect(lambda: navigateFromOutputMode(parent))
    buttons[0].clicked.connect(lambda: changeStacks(parent,getMainWidgetIndex("help"),getBottomIndex("enter only return to output menu")))


    sidebar.setLayout(layout)
    return sidebar