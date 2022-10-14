import sys
from tkinter import Button
from PyQt5.QtWidgets import QWidget, QGridLayout, QLineEdit, QLabel, QStackedWidget
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from UI.OutputMenuPage.outputMenu import OutputMenuUpper
from UI.UI_DEFS import getMainWidgetIndex

from UI.styles import textBoxStyle, promptBoxStyle


from UI.OutputMenuPage.outputMenu import OutputMenuWidget
from UI.KeyboardYNMenuPage.KeyboardYN import KeyboardYNMenuWidget
from UI.YNPage.YN import YesNoWidget
from UI.KeyboardPage.KeyboardWidget import KeyboardWidget
from UI.HelpPage.help import HelpWidget

from UI.KeyboardPage.completer import suggestWords

from UI.Components.enterButton import EnterButton, submitAndReturn

from UI.homeBase import AThread
from PyQt5.QtWidgets import QWidget, QHBoxLayout
from UI.Components.button_container import ButtonContainer
from UI.helperFunctions import disableOtherButtons, changeStacks
# from symbol import or_test
from UI.status import setCurrentPage
from UI.KeyboardPage.KeyboardWidget import keyboardClick, toggle, space, backspace


class MainContainer(QWidget):
    def __init__(self, parent):
        super().__init__()

        layout = QGridLayout()
        self.setLayout(layout)
        
        self.myThread = AThread()
        self.myThread.start()

        #TODO: fix server comm integration
        #self.parent = parent

        width = 5
        textFieldWidth = 3
        # height = 6
        mainWidget = mainStack(self)
        
        #UPPER SECTION
        layout.addWidget(promptBox("What did you have for dinner last night?"), 0, 0, 1, textFieldWidth)
        layout.addWidget(inputBox(self), 1, 0, 1, textFieldWidth)

        layout.addWidget(EnterButton(self), 0, 3, 2, width-textFieldWidth)
        #MIDDLE SECTION
        layout.addWidget(mainWidget, 2, 0, 2, width)

        self.initUI()

        self.myThread.enterButtonSig.connect(self.onEnterButton)

        self.myThread.helpPageSig.connect(self.onHelpPage)
        self.myThread.voicePageSig.connect(self.onVoice)
        self.myThread.twitterPageSig.connect(self.onTwitter)

        self.myThread.keyboardPageSig.connect(self.onOutputKeyboard)
        self.myThread.ynPageSig.connect(self.onOutputYN)

        # self.myThread.yesNoPageSig.connect(self.onYesNoPage)
        self.myThread.returnHomeSig.connect(self.onReturnHome)

        self.myThread.yesSig.connect(self.onYes)
        self.myThread.noSig.connect(self.onNo)

        self.myThread.keyboardUpButOne.connect(self.onUpButOne)
        self.myThread.keyboardUpButTwo.connect(self.onUpButTwo)
        self.myThread.keyboardUpButThree.connect(self.onUpButThree)
        self.myThread.keyboardUpButFour.connect(self.onUpButFour)

        self.myThread.spaceSig.connect(self.onSpace)
        self.myThread.backspaceSig.connect(self.onBackspace)
        self.myThread.toggleSig.connect(self.onToggle)
    
    def onVoice(self):
        outputVoice(self)

    def onEnterButton(self):
        enterButton(self)

    def onOutputKeyboard(self):
        outputKeyboard(self)

    def onHelpPage(self):
        help(self)

    def onTwitter(self):
        outputTwitter(self)

    def onOutputYN(self):
        outputYN(self)

    def onReturnHome(self):
        returnHome(self)

    def onYes(self):
        yes(self)
    
    def onNo(self):
        no(self)

    def onUpButOne(self):
        upButOne(self)
    
    def onUpButTwo(self):
        upButTwo(self)

    def onUpButThree(self):
        upButThree(self)

    def onUpButFour(self):
        upButFour(self)

    def onSpace(self):
        spaceButton(self)

    def onToggle(self):
        toggleButton(self)
    
    def onBackspace(self):
        backspaceButton(self)

    def initUI(self):
        self.setGeometry(100, 100, 900, 900)
        self.setWindowTitle('Icon')
        self.setWindowIcon(QIcon('web.png'))

        self.show()

def enterButton(self):
    enter = self.findChild(ButtonContainer, "Enter Button")
    # print(enter)
    submitAndReturn(enter, self)

def help(self):
    print("helped")
    
    changeStacks(self ,getMainWidgetIndex("Help Page"))

def promptBox(text=""):
    prompt = QLabel(text)
    prompt.setStyleSheet(promptBoxStyle)
    prompt.setAlignment(QtCore.Qt.AlignCenter)
    prompt.setObjectName("Prompt")
    return prompt


def inputBox(parent):
    textbox = QLineEdit()
    textbox.setStyleSheet(textBoxStyle)
    textbox.setObjectName("Input")
    # textbox.textChanged.connect(lambda: suggestWords(parent))
    return textbox


def mainStack(parent):
    stack = QStackedWidget()
    stack.setObjectName("Main Widget")
    # stack.setStyleSheet(mainButtonStyle)

    stack.addWidget(OutputMenuWidget(parent))  # 0
    stack.addWidget(KeyboardYNMenuWidget(parent))  # 1
    
    stack.addWidget(YesNoWidget(parent))  # 2
    stack.addWidget(KeyboardWidget(parent))  # 3
    stack.addWidget(HelpWidget(parent))  # 4

    return stack

def outputVoice(self):
    main = self.findChild(QStackedWidget, "Main Widget")
    outputMenu = main.findChild(QWidget, "Output Menu Page")
    upperMenu = outputMenu.findChild(QWidget, "Upper Menu")

    buttons = upperMenu.findChildren(ButtonContainer)

    buttons[1].setChecked(True)
    disableOtherButtons(buttons, buttons[1])


def outputTwitter(self):
    main = self.findChild(QStackedWidget, "Main Widget")
    outputMenu = main.findChild(QWidget, "Output Menu Page")
    upperMenu = outputMenu.findChild(QWidget, "Upper Menu")

    buttons = upperMenu.findChildren(ButtonContainer)

    buttons[0].setChecked(True)
    disableOtherButtons(buttons, buttons[0])


def outputKeyboard(self):
    main = self.findChild(QStackedWidget, "Main Widget")
    menuWidget = main.findChild(QWidget, "Keyboard YN Menu Page")
    upperMenu = menuWidget.findChild(QWidget, "upper menu")

    buttons = upperMenu.findChildren(ButtonContainer)

    buttons[0].setChecked(True)
    disableOtherButtons(buttons, buttons[0])

def outputYN(self):
    main = self.findChild(QStackedWidget, "Main Widget")
    menuWidget = main.findChild(QWidget, "Keyboard YN Menu Page")
    upperMenu = menuWidget.findChild(QWidget, "upper menu")

    buttons = upperMenu.findChildren(ButtonContainer)

    buttons[1].setChecked(True)
    disableOtherButtons(buttons, buttons[1])

def returnHome(self):
    changeStacks(self, getMainWidgetIndex("Output Menu Page"))

def yes(self):
    main = self.findChild(QStackedWidget, "Main Widget")
    YNpage = main.findChild(QWidget, "YN Page")

    buttons = YNpage.findChildren(ButtonContainer)

    buttons[0].setChecked(True)
    disableOtherButtons(buttons, buttons[0])

def no(self):
    main = self.findChild(QStackedWidget, "Main Widget")
    YNpage = main.findChild(QWidget, "YN Page")

    buttons = YNpage.findChildren(ButtonContainer)

    buttons[1].setChecked(True)
    disableOtherButtons(buttons, buttons[1])

def upButOne(self):
    main = self.findChild(QStackedWidget, "Main Widget")
    page = main.findChild(QWidget, "Keyboard Page")
    keyboard = page.findChild(QWidget, "Keyboard Widget")

    buttons = keyboard.findChildren(ButtonContainer)

    keyboardClick(self, buttons, buttons[0])

def upButTwo(self):
    main = self.findChild(QStackedWidget, "Main Widget")
    page = main.findChild(QWidget, "Keyboard Page")
    keyboard = page.findChild(QWidget, "Keyboard Widget")

    buttons = keyboard.findChildren(ButtonContainer)

    keyboardClick(self, buttons, buttons[1])

def upButThree(self):
    main = self.findChild(QStackedWidget, "Main Widget")
    page = main.findChild(QWidget, "Keyboard Page")
    keyboard = page.findChild(QWidget, "Keyboard Widget")
    
    buttons = keyboard.findChildren(ButtonContainer)
    
    keyboardClick(self, buttons, buttons[2])

def upButFour(self):
    main = self.findChild(QStackedWidget, "Main Widget")
    page = main.findChild(QWidget, "Keyboard Page")
    keyboard = page.findChild(QWidget, "Keyboard Widget")
    
    buttons = keyboard.findChildren(ButtonContainer)
    
    keyboardClick(self, buttons, buttons[3])

def spaceButton(self):
    space(self)
    
def toggleButton(self):
    toggle(self)

def backspaceButton(self):
    backspace(self)

