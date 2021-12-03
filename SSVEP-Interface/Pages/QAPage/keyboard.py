from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QGridLayout, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from pynput.keyboard import Key, Controller
import sys

from Pages.QAPage.search import SearchWidget


class KeyboardInput(QMainWindow):
    def __init__(self):
        super(KeyboardInput, self).__init__()

        self.setWindowTitle('Toggle Testing')  # Sets name of window
        # Sets location (x, y) and size (width, height) of current window
        self.setGeometry(0, 0, 1600, 900)

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

    def alpha_keyboard_click(self):  # clicking a button in the keyboard view
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

        # Create the toggle/mode switch
        self.toggle = QPushButton(self)
        self.toggle.setText("Toggle Mode")
        self.toggle.clicked.connect(self.toggleClick)
        self.toggle.setFixedWidth(200)

        self.generalLayout.addWidget(self.toggle, alignment=Qt.AlignRight)

    def _createDisplay(self):
        """Create the display."""
        # Create the display widget
        self.display = SearchWidget()
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
                   '4 | 5 | 6 | 7 | 8 | 9': (1, 2),  # problem: we can't have 0
                   }
        # Create the buttons and add them to the grid layout
        for btnText, pos in buttons.items():
            self.buttons[btnText] = QPushButton(btnText)
            self.buttons[btnText].setFixedSize(500, 200)
            self.buttons[btnText].clicked.connect(self.alpha_keyboard_click)
            buttonsLayout.addWidget(self.buttons[btnText], pos[0], pos[1])
        # Add buttonsLayout to the general layout
        self.generalLayout.addLayout(buttonsLayout)

    def setWordMode(self):  # set button text to "list of suggested words"
        self.label.setText("word mode")
        # list of suggested words (given by OpenAI integration)
        self.wordLabels = ["Hi", "Bruh", "I'm ok",
                           "Good, and you?", "Duck Duck Goose ", "MIT of the North"]
        i = 0
        for btnText in self.buttons.keys():
            self.buttons[btnText].setText(self.wordLabels[i])
            i += 1

    def setAlphaMode(self):  # set button text to alphabet
        self.label.setText("keyboard mode")
        for btnText in self.buttons.keys():
            self.buttons[btnText].setText(btnText)
            # cancels any previous signals and ensure that each keyboard press ONLY lead to char input
            self.buttons[btnText].clicked.disconnect()
            self.buttons[btnText].clicked.connect(self.alpha_keyboard_click)

    def setChars(self, letters):  # set button text to characters for input
        self.label.setText("char mode")
        charList = list(letters.split(' | '))
        i = 0
        for btnText in self.buttons.keys():
            self.buttons[btnText].setText(charList[i])
            i += 1
            # cancels signal to trigger char input mode
            self.buttons[btnText].clicked.disconnect()
            # upon any keyboard presses, return to alpha view and set display
            self.buttons[btnText].clicked.connect(self.setDisplayText)

    def setDisplayText(self):
        """Set display's text."""
        self.sending_button = self.sender()
        text = self.sending_button.text()

        self.display.setFocus()

        keyboard = Controller()
        for key in text:
            keyboard.press(key)
            keyboard.release(key)

        # return to keyboard view
        self.setAlphaMode()
        self.toggle.setText("Toggle Mode")


if __name__ == '__main__':

    app = QApplication(sys.argv)
    win = KeyboardInput()
    win.show()
    sys.exit(app.exec_())