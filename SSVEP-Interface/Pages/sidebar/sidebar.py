from locale import currency
from tkinter import Button
from PyQt5.QtWidgets import QLabel,QWidget,QLineEdit,QStackedWidget,QVBoxLayout
from Pages.sidebar.enterButton import EnterButton
from Pages.styles import mainButtonStyle
from Pages.button_container import ButtonContainer

class Sidebar(QStackedWidget):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.setObjectName("Sidebar Stack")

        self.addWidget(homeSidebar(parent))  # 0
        self.addWidget(characterSidebar(parent))  # 1
        self.addWidget(enterOnlySidebar(parent))  # 2

    
def homeSidebar(parent):
    sidebar = QWidget()
    layout = QVBoxLayout()

    buttons = []

    buttons.append(EnterButton(parent))
    buttons.append(ButtonContainer("Help",checkable=False))
    
    for button in buttons:
        layout.addWidget(button)

    buttons[0].clicked.connect(lambda: navigateFromHome(parent))
    buttons[1].clicked.connect(lambda: changeStacks(parent,4,2))


    sidebar.setLayout(layout)
    return sidebar

def navigateFromHome(parent):
    
    labels = ["MC","YN","Type"]
    mainButtons = [parent.findChild(ButtonContainer,label) for label in labels]

    for button in mainButtons:
        if button.label.text() == labels[0] and button.isChecked():
            print("going to MC")
            button.setChecked(False)
            changeStacks(parent,1,2)
        elif button.label.text() == labels[1] and button.isChecked():
            print("going to YN")
            button.setChecked(False)
            changeStacks(parent,2,2)
        elif button.label.text() == labels[2] and button.isChecked():
            print("going to Typing")
            button.setChecked(False)
            changeStacks(parent,3,1)


def characterSidebar(parent):
    sidebar = QWidget()
    layout = QVBoxLayout()
    buttons = []

    # buttons.append(ButtonContainer("Enter Message",checkable=False,red=0,blue=0))
    buttons.append(EnterButton(parent))
    buttons.append(ButtonContainer("Backspace",checkable=False))
    buttons.append(ButtonContainer("Space",checkable=False,red=0,green=0))
    buttons.append(ButtonContainer("Toggle",checkable=False))

    for button in buttons:
        layout.addWidget(button)

    buttons[0].clicked.connect(lambda: changeStacks(parent,0,0))
    buttons[1].clicked.connect(lambda: backspace(parent))
    buttons[2].clicked.connect(lambda: space(parent))

    sidebar.setLayout(layout)
    return sidebar


def enterOnlySidebar(parent):
    # For MC Page and Yes/No Page
    sidebar = QWidget()
    layout = QVBoxLayout()
    layout.addWidget(EnterButton(parent))
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

def space(parent):
    inputField = parent.findChild(QLineEdit,"Input")

    temp = inputField.text() + " "
    inputField.setText(temp)