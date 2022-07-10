from cgitb import enable
from locale import currency
from tkinter import Button
from PyQt5.QtWidgets import QLabel,QWidget,QLineEdit,QStackedWidget,QVBoxLayout
from Pages.sidebar.enterButton import EnterButton
from Pages.styles import mainButtonStyle
from Pages.button_container import ButtonContainer
from Pages.QAPage.completer2 import suggestWords
from Pages.QAPage.keyboard2 import groupedChars
import Pages.sidebar.enterButton


from Pages.HomePage.mainWidgetIndexes import getMainWidgetIndex
from Pages.sidebar.sidebarIndexes import getSidebarIndex

#indexes
class Sidebar(QStackedWidget):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.setObjectName("Sidebar Stack")

        self.addWidget(OutputModeSidebar(parent))  # 0
        self.addWidget(homeSidebar(parent))  # 1
        self.addWidget(characterSidebar(parent))  # 2
        self.addWidget(enterOnlySidebar(parent))  # 3
        self.addWidget(enterReturnToOutputModeSidebar(parent))  # 4

def OutputModeSidebar(parent):
    sidebar = QWidget()
    layout = QVBoxLayout()

    buttons = []

    buttons.append(EnterButton(parent))
    buttons.append(ButtonContainer("Help",checkable=False))
    
    for button in buttons:
        layout.addWidget(button)

    buttons[0].clicked.connect(lambda: navigateFromOutputMode(parent))
    buttons[1].clicked.connect(lambda: changeStacks(parent,getMainWidgetIndex("help"),getSidebarIndex("enter only return to output mode")))


    sidebar.setLayout(layout)
    return sidebar
    
def homeSidebar(parent):
    sidebar = QWidget()
    layout = QVBoxLayout()

    buttons = []

    buttons.append(EnterButton(parent))
    buttons.append(ButtonContainer("Help",checkable=False))
    buttons.append(ButtonContainer("Output Toggle",checkable=False))
    
    for button in buttons:
        layout.addWidget(button)

    buttons[0].clicked.connect(lambda: navigateFromHome(parent))
    buttons[1].clicked.connect(lambda: changeStacks(parent,getMainWidgetIndex("help"),getSidebarIndex("enter only")))
    buttons[2].clicked.connect(lambda: changeStacks(parent,getMainWidgetIndex("output mode"),getSidebarIndex("output mode")))


    sidebar.setLayout(layout)
    return sidebar

def navigateFromOutputMode(parent):
    
    labels = ['Twitter','Voice','Server Communication','Visual Communication']
    mainButtons = [parent.findChild(ButtonContainer,label) for label in labels]

    for button in mainButtons:
        if button.label.text() == labels[0] and button.isChecked():
            print("going to Twitter")
            button.setChecked(False)
            Pages.sidebar.enterButton.outputMode = "twitter"
            changeStacks(parent,getMainWidgetIndex("home"),getSidebarIndex("home"))
        elif button.label.text() == labels[1] and button.isChecked():
            print("going to Voice")
            button.setChecked(False)
            Pages.sidebar.enterButton.outputMode = "voice"
            # changeStacks(parent,2,2)
        elif button.label.text() == labels[2] and button.isChecked():
            print("going to Server Communication")
            button.setChecked(False)
            Pages.sidebar.enterButton.outputMode = "server"
            # changeStacks(parent,3,1)
        elif button.label.text() == labels[3] and button.isChecked():
            print("going to Visual Communication")
            button.setChecked(False)
            Pages.sidebar.enterButton.outputMode = "visual"
            # changeStacks(parent,3,1)

def navigateFromHome(parent):
    
    labels = ["MC","YN","Type"]
    mainButtons = [parent.findChild(ButtonContainer,label) for label in labels]

    for button in mainButtons:
        if button.label.text() == labels[0] and button.isChecked():
            print("going to MC")
            button.setChecked(False)
            changeStacks(parent,getMainWidgetIndex("mc"),getSidebarIndex("enter only"))
        elif button.label.text() == labels[1] and button.isChecked():
            print("going to YN")
            button.setChecked(False)
            changeStacks(parent,getMainWidgetIndex("yn"),getSidebarIndex("enter only"))
        elif button.label.text() == labels[2] and button.isChecked():
            print("going to Typing")
            button.setChecked(False)
            changeStacks(parent,getMainWidgetIndex("keyboard"),getSidebarIndex("character only"))


def characterSidebar(parent):
    sidebar = QWidget()
    layout = QVBoxLayout()
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

    # buttons[0].clicked.connect(lambda: changeStacks(parent,getMainWidgetIndex("home"),getSidebarIndex("home")))
    buttons[1].clicked.connect(lambda: backspace(parent))
    buttons[2].clicked.connect(lambda: space(parent))
    buttons[3].clicked.connect(lambda: toggle(parent))

    sidebar.setLayout(layout)
    return sidebar


def enterOnlySidebar(parent):
    # For MC Page and Yes/No Page
    sidebar = QWidget()
    layout = QVBoxLayout()
    layout.addWidget(EnterButton(parent))
    sidebar.setLayout(layout)
    return sidebar

def enterReturnToOutputModeSidebar(parent):
    # For MC Page and Yes/No Page
    sidebar = QWidget()
    layout = QVBoxLayout()
    btn = ButtonContainer("Enter",checkable=False)
    btn.clicked.connect(lambda: changeStacks(parent, getMainWidgetIndex("output mode"), getSidebarIndex("output mode")))
    layout.addWidget(btn)
    sidebar.setLayout(layout)
    return sidebar


def changeStacks(parent,mainIndex,sidebarIndex):
    mainStack = parent.findChild(QStackedWidget,"Main Stack")
    sidebarStack = parent.findChild(QStackedWidget,"Sidebar Stack")

    mainStack.setCurrentIndex(mainIndex)
    sidebarStack.setCurrentIndex(sidebarIndex)


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

