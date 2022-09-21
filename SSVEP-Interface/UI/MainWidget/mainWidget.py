import sys
from PyQt5.QtWidgets import QWidget, QGridLayout, QLineEdit, QLabel, QStackedWidget
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore

from UI.styles import textBoxStyle, promptBoxStyle


from UI.OutputMenuPage.outputMenu import OutputMenuWidget
from UI.KeyboardYNMenuPage.KeyboardYN import KeyboardYNMenuWidget
from UI.YNPage.YN import YesNoWidget
from UI.KeyboardPage.KeyboardWidget import KeyboardWidget
from UI.HelpPage.help import HelpWidget

from UI.KeyboardPage.completer import suggestWords

from UI.Components.enterButton import EnterButton

class MainWidgetContainer(QWidget):
    def __init__(self, parent):
        super().__init__()

        layout = QGridLayout()
        self.setLayout(layout)
        
        #TODO: fix server comm integration
        #self.parent = parent

        width = 5
        textFieldWidth = 3
        # height = 6
        mainWidget = mainStack(self)
        
        #UPPER SECTION
        layout.addWidget(title(), 0, 0, 1, 1)
        layout.addWidget(promptBox("What did you have for dinner last night?"), 1, 0, 1, textFieldWidth)
        layout.addWidget(inputBox(self), 2, 0, 1, textFieldWidth)

        layout.addWidget(EnterButton(self), 0, 3, 3, width-textFieldWidth)
        #MIDDLE SECTION
        layout.addWidget(mainWidget, 3, 0, 2, width)

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 900, 900)
        self.setWindowTitle('Icon')
        self.setWindowIcon(QIcon('web.png'))

        self.show()


def title():
    title = QLabel("test")
    title.setObjectName("Title")
    title.setMaximumHeight(40)
    return title


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


