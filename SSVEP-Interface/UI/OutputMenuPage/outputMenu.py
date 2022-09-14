from tkinter.ttk import Button
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout

from UI.Components.button_container import ButtonContainer

from UI.UI_DEFS import getMainWidgetIndex


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

    button = ButtonContainer("Help",freqName="Output Menu Help",checkable=False)
    
    layout.addWidget(button)

    button.clicked.connect(lambda: changeStacks(parent,getMainWidgetIndex("Help Page")))

    # button.stimuli.toggleOff()

    sidebar.setLayout(layout)
    return sidebar