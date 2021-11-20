
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget,QApplication, QMainWindow,QLineEdit, QGridLayout, QVBoxLayout

class keyboardInput(QMainWindow):
    def __init__(self):
        super(keyboardInput,self).__init__()

        self.setWindowTitle('Toggle Testing') # Sets name of window
        self.setGeometry(0, 0, 1600, 900) # Sets location (x, y) and size (width, height) of current window

        self.generalLayout = QVBoxLayout()
        self.generalLayout.setAlignment(Qt.AlignCenter)

        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        self.initUI()
        
    def toggleClick(self):
        if self.label.text() == "keyboard mode":
            self.setWordMode()
        elif self.label.text() == "word mode" or self.label.text() == "char mode" or self.toggle.text() == "Return":
            self.toggle.setText("Toggle Mode")
            self.setAlphaMode()

    def alpha_keyboard_click(self):
        if self.label.text() == "keyboard mode":
            self.toggle.setText("Return")
            self.sending_button = self.sender()
            letters = self.sending_button.text()
            self.setChars(letters)

    # create UI elements
    def initUI(self):
        # temporary mode indicator label
        self.label = QLabel(self)
        self.label.setText("keyboard mode")
        self.label.setFixedHeight(35)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("border: 1px solid black; font-weight: 600;")
        self.generalLayout.addWidget(self.label)

        self._createDisplay()

        # Create the keyboard buttons
        self._createButtons()

        # Create the toggle
        self.toggle = QPushButton(self)
        self.toggle.setText("Toggle Mode")
        self.toggle.clicked.connect(self.toggleClick)
        self.toggle.setFixedWidth(200)
  

        self.generalLayout.addWidget(self.toggle, alignment=Qt.AlignRight)

    def _createDisplay(self):
        """Create the display."""
        # Create the display widget
        self.display = QLineEdit()
        # Set some display's properties
        self.display.setFixedHeight(35)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        # Add the display to the general layout
        self.generalLayout.addWidget(self.display)

    def _createButtons(self):
        """Create the keyboard buttons."""
        self.buttons = {}
        buttonsLayout = QGridLayout()
        # Button text | position on the QGridLayout
        buttons = {'a | b | c | d | e | f': (0, 0),
                   'g | h | i | j | k | l': (0, 1),
                   'm | n | o | p | q | r': (0, 2),
                   'r | s | t | u | v | w': (1, 0),
                   'x | y | z | 1 | 2 | 3': (1, 1),
                   '4 | 5 | 6 | 7 | 8 | 9': (1, 2), # problem: we can't have 0 
                  }
        # Create the buttons and add them to the grid layout
        for btnText, pos in buttons.items():
            self.buttons[btnText] = QPushButton(btnText)
            self.buttons[btnText].setFixedSize(500, 200)
            self.buttons[btnText].clicked.connect(self.alpha_keyboard_click)
            buttonsLayout.addWidget(self.buttons[btnText], pos[0], pos[1])
        # Add buttonsLayout to the general layout
        self.generalLayout.addLayout(buttonsLayout)


    def setWordMode(self): # set button text to "list of suggested words"
        self.label.setText("word mode")
        self.wordLabels = ["Hi", "Bruh", "I'm ok", "Good, and you?", "Duck Duck Goose ", "MIT of the North"] # list of suggested words (given by OpenAI integration)
        i = 0
        for btnText in self.buttons.keys():
            self.buttons[btnText].setText(self.wordLabels[i])
            i += 1

    def setAlphaMode(self): # set button text to alphabet 
        self.label.setText("keyboard mode")
        for btnText in self.buttons.keys():
            self.buttons[btnText].setText(btnText)
            self.buttons[btnText].clicked.disconnect() # cancels any previous signals and ensure that each keyboard press ONLY lead to char input
            self.buttons[btnText].clicked.connect(self.alpha_keyboard_click)


    def setChars(self, letters): # set button text to characters for input
        self.label.setText("char mode")
        charList = list(letters.split(' | '))
        i = 0
        for btnText in self.buttons.keys():
            self.buttons[btnText].setText(charList[i])
            i += 1
            self.buttons[btnText].clicked.disconnect() # cancels signal to trigger char input mode
            self.buttons[btnText].clicked.connect(self.setDisplayText) # upon any keyboard presses, return to alpha view and set display

    def setDisplayText(self):
        """Set display's text."""   
        self.sending_button = self.sender()
        text = self.sending_button.text()
        self.display.setText(f"{self.displayText()}{text}")
        self.display.setFocus()
        # return to keyboard view
        self.setAlphaMode() 
        self.toggle.setText("Toggle Mode")


    def displayText(self):
        """Get display's text."""
        return self.display.text()

    def clearDisplay(self):
        """Clear the display."""
        self.setDisplayText('')

class QuestionAndAnswerWidget(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        layout = self._createLayout(parent)
        self.setLayout(layout)

    # Method creates the layout of the page, called in the init function to maintain clean and readable code
    # If you are changing the functionalities of the page, you will most likely want to alter this method
    def _createLayout(self, parent):
        layout = QHBoxLayout() # Creates a verticle template that formats whatever widgets are added to it
        layout.setSpacing(0)
        layout.setContentsMargins(100, 100, 100, 100)    
        centerWidget = keyboardInput()
        button2 = self._createBackButton(text=">")
        button2.clicked.connect(parent.showTF)
        button1 = self._createBackButton(text="<")
        button1.clicked.connect(parent.showHome)
        layout.addWidget(button1)
        layout.addWidget(centerWidget)
        layout.addWidget(button2)
        layout.setAlignment(Qt.AlignVCenter)
        return layout

    
    # def _createCenterText(self):
    #     centertext = QLabel("Question And Answer Page!")
    #     centertext.setMaximumHeight(100)
    #     centertext.setFont(QFont('Arial', 32))
    #     centertext.setAlignment(Qt.AlignCenter)
    #     return centertext
    
    
    def _createBackButton(self, text):
        button = QPushButton(text)
        button.setMinimumHeight(150)
        button.setMaximumWidth(20)
        return button
