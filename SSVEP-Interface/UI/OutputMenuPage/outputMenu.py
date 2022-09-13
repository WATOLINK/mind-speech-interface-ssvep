from PyQt5.QtWidgets import QApplication, QButtonGroup, QWidget, QGridLayout, QLineEdit, QLabel, QPushButton, QStackedWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore

from UI.styles import textBoxStyle, sideBarStyle, mainButtonStyle, promptBoxStyle, instructionsStyle
from UI.Components.button_container import ButtonContainer
from UI.KeyboardPage.KeyboardWidget import KeyboardWidget
from UI.HelpPage.help import HelpWidget
from UI.KeyboardPage.completer2 import suggestWords

from UI.Components.enterButton import EnterButton

from UI.UI_DEFS import getMainWidgetIndex, MainWidgetIndexes


from UI.helperFunctions import disableOtherButtons, changeStacks


def OutputMenuWidget(parent):
    outputMode = QWidget()
    layout = QVBoxLayout()
    outputMode.setObjectName("Output Menu Page")
    layout.addWidget(OutputMenuUpper(parent))
    layout.addWidget(OutputMenuLower(parent))
    outputMode.setLayout(layout)
    return outputMode


def OutputMenuUpper(parent):
    outputMode = QWidget()
    layout = QHBoxLayout()
    outputMode.setObjectName("Output Menu")

    labels = ['Twitter','Voice','Visual Communication']
    buttons = []

    for x in range(len(labels)):
        button = ButtonContainer(labels[x],freqName=f"Output Menu {x+1}")
        button.setObjectName(labels[x])
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

def OutputMenuLower(parent):
    sidebar = QWidget()
    layout = QHBoxLayout()

    buttons = []

    buttons.append(ButtonContainer("Help",freqName="Output Menu Help",checkable=False))
    
    for button in buttons:
        layout.addWidget(button)

    buttons[0].clicked.connect(lambda: changeStacks(parent,getMainWidgetIndex("Help Page")))


    sidebar.setLayout(layout)
    return sidebar