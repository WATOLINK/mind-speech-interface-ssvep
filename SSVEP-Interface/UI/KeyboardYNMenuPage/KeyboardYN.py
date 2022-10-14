from PyQt5.QtWidgets import QWidget, QStackedWidget, QHBoxLayout, QVBoxLayout

from UI.Components.button_container import ButtonContainer

from UI.UI_DEFS import getMainWidgetIndex

from UI.helperFunctions import disableOtherButtons, changeStacks

from UI.status import setOutputMode


def KeyboardYNMenuWidget(parent):
    outputMode = QWidget()
    layout = QVBoxLayout()
    outputMode.setObjectName("Keyboard YN Menu Page")
    layout.addWidget(KeyboardYNMenuUpper(parent))
    layout.addWidget(KeyboardYNMenuLower(parent))
    outputMode.setLayout(layout)
    return outputMode

def KeyboardYNMenuUpper(parent):
    menu = QWidget()
    layout = QHBoxLayout()

    menu.setObjectName("upper menu")
    # DO NOT CHANGE RIGHT NOW
    labels = ['Use Keyboard', 'Use Yes/No']
    buttons = []

    for x in range(len(labels)):
        button = ButtonContainer(labels[x],freqName=f"Keyboard YN Menu {x+1}") 
        button.setObjectName(labels[x])
        buttons.append(button)
        layout.addWidget(button)

    buttons[0].clicked.connect(
        lambda: disableOtherButtons(buttons, buttons[0]))
    buttons[1].clicked.connect(
        lambda: disableOtherButtons(buttons, buttons[1]))

    menu.setLayout(layout)
    return menu


def KeyboardYNMenuLower(parent):
    sidebar = QWidget()
    layout = QHBoxLayout()

    buttons = []

    # buttons.append(ButtonContainer("Help",freqName="Keyboard YN Menu Help",checkable=False))
    buttons.append(ButtonContainer("Back to Menu",freqName="Back to Output Menu",checkable=False))
    
    for button in buttons:
        layout.addWidget(button)

    # buttons[0].clicked.connect(lambda: changeStacks(parent,getMainWidgetIndex("Help Page")))
    buttons[0].clicked.connect(lambda: returnToOutputMenu(parent))


    sidebar.setLayout(layout)
    return sidebar

def returnToOutputMenu(parent):
    mainStack = parent.findChild(QStackedWidget,"Main Widget")
    setOutputMode("")
    currWidget = mainStack.currentWidget()

    if currWidget.objectName() == "Keyboard YN Menu Page":
        for button in currWidget.findChildren(ButtonContainer):
            if button.isChecked():
                button.setChecked(False)

    changeStacks(parent,getMainWidgetIndex("Output Menu Page"))