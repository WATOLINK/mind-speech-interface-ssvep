from inspect import stack
import sys
from PyQt5.QtWidgets import QApplication, QButtonGroup, QWidget, QGridLayout, QLineEdit, QLabel, QPushButton, QStackedWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore

from Pages.styles import textBoxStyle, sideBarStyle, mainButtonStyle, promptBoxStyle


class HomePageWidget(QWidget):

    def __init__(self, parent):
        super().__init__()

        layout = QGridLayout()
        self.setLayout(layout)

        width = 4
        height = 6

        layout.addWidget(promptBox(),0,0,1,3)
        layout.addWidget(inputBox(),1,0,1,3)
        layout.addWidget(mainStack(),2,0,4,3)
        layout.addWidget(sideBar(),0,4,height,1)


        self.initUI()


    def initUI(self):

        self.setGeometry(100, 100, 900, 900)
        self.setWindowTitle('Icon')
        self.setWindowIcon(QIcon('web.png'))

        self.show()

def promptBox():
    prompt = QLabel("AMONG US")
    prompt.setStyleSheet(promptBoxStyle)
    prompt.setAlignment(QtCore.Qt.AlignCenter)
    return prompt

def inputBox():
    textbox = QLineEdit()
    textbox.setStyleSheet(textBoxStyle)
    return textbox

def mainStack():
    stack = QStackedWidget()
    stack.setStyleSheet(mainButtonStyle)

    stack.addWidget(homeWidget(stack))             #0
    stack.addWidget(multipleChoiceWidget())        #1
    stack.addWidget(yesNoWidget())                 #2
    stack.addWidget(groupedCharacterWidget(stack)) #3
    stack.addWidget(individualCharacters1Widget(stack)) #4
    stack.addWidget(individualCharacters2Widget(stack)) #5
    stack.addWidget(individualCharacters3Widget(stack)) #6
    stack.addWidget(individualCharacters4Widget(stack)) #7
    stack.addWidget(individualCharacters5Widget(stack)) #8
    stack.addWidget(individualCharacters6Widget(stack)) #9

    return stack

def homeWidget(mainStack):
    home = QWidget()
    layout = QHBoxLayout()


    button_group = QButtonGroup()

    titles = ['MC', 'YN', 'Type']
    buttons = [QPushButton(title) for title in titles]


    for button in buttons:
        layout.addWidget(button)
        button_group.addButton(button)
        button.setCheckable(True)
    
    for button in buttons:
        print(button.text())

    buttons[0].clicked.connect(lambda: disableOtherButton(button_group,buttons[0]))
    buttons[1].clicked.connect(lambda: disableOtherButton(button_group,buttons[1]))
    buttons[2].clicked.connect(lambda: disableOtherButton(button_group,buttons[2]))

    home.setLayout(layout)
    return home

def disableOtherButton(buttonGroup,selected):
    if selected.isChecked():
        for button in buttonGroup.buttons():
            if button != selected:
                button.setChecked (False)


def multipleChoiceWidget():
    widget = QWidget()
    layout = QGridLayout()
    widget.setLayout(layout)
    labels = [["A","B"], ["C","D"]]
    for row in range(len(labels)):
        for col in range(len(labels[0])):
            layout.addWidget(QPushButton(labels[row][col]), row, col)

    return widget

def yesNoWidget():
    widget = QWidget()
    layout = QHBoxLayout()
    labels = ["Yes/True", "No/False"]
    for col in range(len(labels)):
        layout.addWidget(QPushButton(labels[col]))
    widget.setLayout(layout)
    return widget

def groupedCharacterWidget(mainStack):
    widget = QWidget()
    layout = QGridLayout()
    labels = ["ABCDEF", "GHIJKL", "MNOPQR","STUVWX", "YZ0123", "456789"]


    buttonArray = []
    for x in range(6):
        button = QPushButton(labels[x])
        buttonArray.append(button)
        layout.addWidget(button, int(x/3), x%3)

    # when you do this with a for loop, it dont wory, we don't know why
    # but hardcoding works! so haha!
    buttonArray[0].clicked.connect(lambda : mainStack.setCurrentIndex(4))
    buttonArray[1].clicked.connect(lambda : mainStack.setCurrentIndex(5))
    buttonArray[2].clicked.connect(lambda : mainStack.setCurrentIndex(6))
    buttonArray[3].clicked.connect(lambda : mainStack.setCurrentIndex(7))
    buttonArray[4].clicked.connect(lambda : mainStack.setCurrentIndex(8))
    buttonArray[5].clicked.connect(lambda : mainStack.setCurrentIndex(9))

    widget.setLayout(layout)
    return widget

def individualCharacters1Widget(mainStack):
    widget = QWidget()
    layout = QGridLayout()
    labels = [["A", "B", "C"], ["D", "E", "F"]]
    for row in range(len(labels)):
        for col in range(len(labels[0])):
            button = QPushButton(labels[row][col])
            button.clicked.connect(lambda : mainStack.setCurrentIndex(3))
            layout.addWidget(button, row, col)
    widget.setLayout(layout)
    return widget

def individualCharacters2Widget(mainStack):
    widget = QWidget()
    layout = QGridLayout()
    labels = [["G", "H", "I"], ["J", "K", "L"]]
    for row in range(len(labels)):
        for col in range(len(labels[0])):
            button = QPushButton(labels[row][col])
            button.clicked.connect(lambda : mainStack.setCurrentIndex(3))
            layout.addWidget(button, row, col)
    widget.setLayout(layout)
    return widget

def individualCharacters3Widget(mainStack):
    widget = QWidget()
    layout = QGridLayout()
    labels = [["M", "N", "O"], ["P", "Q", "R"]]
    for row in range(len(labels)):
        for col in range(len(labels[0])):
            button = QPushButton(labels[row][col])
            button.clicked.connect(lambda : mainStack.setCurrentIndex(3))
            layout.addWidget(button, row, col)
    widget.setLayout(layout)
    return widget

def individualCharacters4Widget(mainStack):
    widget = QWidget()
    layout = QGridLayout()
    labels = [["S", "T", "U"], ["V", "W", "X"]]
    for row in range(len(labels)):
        for col in range(len(labels[0])):
            button = QPushButton(labels[row][col])
            button.clicked.connect(lambda : mainStack.setCurrentIndex(3))
            layout.addWidget(button, row, col)
    widget.setLayout(layout)
    return widget

def individualCharacters5Widget(mainStack):
    widget = QWidget()
    layout = QGridLayout()
    labels = [["Y", "Z", "0"], ["1", "2", "3"]]
    for row in range(len(labels)):
        for col in range(len(labels[0])):
            button = QPushButton(labels[row][col])
            button.clicked.connect(lambda : mainStack.setCurrentIndex(3))
            layout.addWidget(button, row, col)
    widget.setLayout(layout)
    return widget

def individualCharacters6Widget(mainStack):
    widget = QWidget()
    layout = QGridLayout()
    labels = [["4", "5", "6"], ["7", "8", "9"]]
    for row in range(len(labels)):
        for col in range(len(labels[0])):
            button = QPushButton(labels[row][col])
            button.clicked.connect(lambda : mainStack.setCurrentIndex(3))
            layout.addWidget(button, row, col)
    widget.setLayout(layout)
    return widget

def sideBar():
    sidebar = QStackedWidget()


    sidebar = QWidget()
    layout = QGridLayout()
    sidebar.setLayout(layout)
    sidebar.setStyleSheet(sideBarStyle)


    for x in range(4):
        layout.addWidget(QPushButton("poop"),x,0)
    return sidebar

def characterSideBar():
    sidebar = QWidget()
    layout = QVBoxLayout()
    labels = ["Enter Message", "Backspace", "Space", "Toggle"]
    for row in range(len(labels)):
        layout.addWidget(QPushButton(labels[row]))
    sidebar.setLayout(layout)
    return sidebar

def characterSideBar():
    sidebar = QWidget()
    layout = QVBoxLayout()
    labels = ["Enter Message", "Backspace", "Space", "Toggle"]
    for row in range(len(labels)):
        layout.addWidget(QPushButton(labels[row]))
    sidebar.setLayout(layout)
    return sidebar

def enterOnlySideBar(mainStack):
    # For MC Page and Yes/No Page
    sidebar = QWidget()
    layout = QVBoxLayout()
    button = QPushButton("Enter")
    button.clicked.connect(lambda : mainStack.setCurrentIndex(0))
    layout.addWidget(button)
    sidebar.setLayout(layout)
    return sidebar
