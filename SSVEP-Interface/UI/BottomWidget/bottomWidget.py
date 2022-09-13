from cgitb import enable
from locale import currency
from tkinter import Button
from PyQt5.QtWidgets import QLabel,QWidget,QLineEdit,QStackedWidget,QVBoxLayout, QHBoxLayout
from UI.styles import mainButtonStyle
from UI.Components.button_container import ButtonContainer
from UI.KeyboardPage.completer2 import suggestWords
from UI.KeyboardPage.keyboard2 import groupedChars
from UI.Components.enterButton import EnterButton

from UI.UI_DEFS import getMainWidgetIndex, MainWidgetIndexes
from UI.BottomWidget.bottomWidgetIndexes import getBottomIndex

from UI.status import setOutputMode, setCurrentPage, printStatus


#indexes
class BottomWidget(QStackedWidget):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.setObjectName("Bottom Widget")

        self.addWidget(helpBottomWidget(parent))  # 0
        self.addWidget(homeBottomWidget(parent))  # 1
        self.addWidget(characterBottomWidget(parent))  # 2
        self.addWidget(enterOnlyBottomWidget(parent))  # 3
        self.addWidget(enterReturnToOutputModeBottomWidget(parent))  # 4

def helpBottomWidget(parent):
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
    
    
def homeBottomWidget(parent):
    sidebar = QWidget()
    layout = QHBoxLayout()

    buttons = []

    # buttons.append(EnterButton(parent))
    buttons.append(ButtonContainer("Help",checkable=False))
    buttons.append(ButtonContainer("Back to Menu",checkable=False))
    
    for button in buttons:
        layout.addWidget(button)

    # buttons[0].clicked.connect(lambda: navigateFromHome(parent))
    buttons[0].clicked.connect(lambda: changeStacks(parent,getMainWidgetIndex("help"),getBottomIndex("enter only")))
    buttons[1].clicked.connect(lambda: outputMenu(parent))


    sidebar.setLayout(layout)
    return sidebar

def outputMenu(parent):
    mainStack = parent.findChild(QStackedWidget,"Main Widget")
    setOutputMode("")
    currWidget = mainStack.currentWidget()

    if currWidget.objectName() == "Keyboard YN Selection Widget":
    # uncheck any checked boxes on submission
        for button in currWidget.findChildren(ButtonContainer):
            if button.isChecked():
                button.setChecked(False)

    changeStacks(parent,getMainWidgetIndex("output menu"),getBottomIndex("output menu"))




def characterBottomWidget(parent):
    sidebar = QWidget()
    layout = QHBoxLayout()
    buttons = []

    # buttons.append(ButtonContainer("Enter Message",checkable=False,red=0,blue=0))
    buttons.append(EnterButton(parent))
    buttons.append(ButtonContainer("Backspace",checkable=False))
    buttons.append(ButtonContainer("Space",checkable=False,red=0,green=0))
    
    toggleBtn = ButtonContainer("Toggle Words",checkable=False)
    toggleBtn.setObjectName("Toggle")
    buttons.append(toggleBtn)

    for button in buttons:
        layout.addWidget(button)

    # buttons[0].clicked.connect(lambda: changeStacks(parent,getMainWidgetIndex("home"),getBottomIndex("home")))
    buttons[0].clicked.connect(lambda: backspace(parent))
    buttons[1].clicked.connect(lambda: space(parent))
    buttons[2].clicked.connect(lambda: toggle(parent))

    sidebar.setLayout(layout)
    return sidebar


def enterOnlyBottomWidget(parent):
    # For MC Page and Yes/No Page
    sidebar = QWidget()
    layout = QHBoxLayout()
    layout.addWidget(EnterButton(parent))
    sidebar.setLayout(layout)
    return sidebar

def enterReturnToOutputModeBottomWidget(parent):
    # For MC Page and Yes/No Page
    sidebar = QWidget()
    layout = QHBoxLayout()
    btn = ButtonContainer("Enter",checkable=False)
    btn.clicked.connect(lambda: changeStacks(parent, getMainWidgetIndex("output menu"), getBottomIndex("output menu")))
    layout.addWidget(btn)
    sidebar.setLayout(layout)
    return sidebar

# FUNCTIONS



def changeStacks(parent,mainIndex,sidebarIndex):
    mainStack = parent.findChild(QStackedWidget,"Main Widget")
    bottomStack = parent.findChild(QStackedWidget,"Bottom Widget")

    mainStack.setCurrentIndex(mainIndex)
    bottomStack.setCurrentIndex(sidebarIndex)
    setCurrentPage(MainWidgetIndexes[mainIndex])

    printStatus()


def backspace(parent):
    inputField = parent.findChild(QLineEdit,"Input")

    temp = inputField.text()

    if len(temp) != 0 :
        inputField.setText(temp[:-1])
        
        #TODO: fix server comm integration
        #parent.parent.emit_message('client_message', {'message': temp[:-1]})

def space(parent):
    inputField = parent.findChild(QLineEdit,"Input")

    temp = inputField.text() + " "
    inputField.setText(temp)
    
    #TODO: fix server comm integration
    #parent.parent.emit_message('client_message', {'message': temp})

def toggle(parent):
    toggleBtn = parent.findChild(ButtonContainer,"Toggle")
    
    if toggleBtn.label.text() == "Toggle Words":
        toggleBtn.label.setText("Toggle Characters")
        suggestWords(parent)
    else:
        toggleBtn.label.setText("Toggle Words")
        keyboardWidget = parent.findChild(QWidget,"Keyboard Widget")
        keyboardBtns = keyboardWidget.findChildren(ButtonContainer)
        
        for x in range(len(keyboardBtns)):
            keyboardBtns[x].label.setText(groupedChars[x])

