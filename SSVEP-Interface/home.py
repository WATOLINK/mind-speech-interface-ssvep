import sys
from PyQt5.QtCore import center, Qt
from PyQt5.QtGui import QFont

from PyQt5.QtWidgets import QApplication, QStackedWidget, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtWidgets import QMainWindow

from Pages.QAPage.qa import QuestionAndAnswerWidget
from Pages.MCPage.mc import MultipleChoiceWidget
from Pages.YNPage.absolute import TrueAndFalseWidget
from Pages.HomePage.homepage import HomePageWidget

from Pages.styles import windowStyle, navigationButtonStyle

class Home(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.generalLayout = QVBoxLayout()
        self.generalLayout.setAlignment(Qt.AlignCenter)

        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

         # Make sure to pass in 'self' to the child widget for it to access parent methods
        self.homePage = HomePageWidget(self)
        self.multiplePage = MultipleChoiceWidget(self)
        self.questionPage = QuestionAndAnswerWidget(self)
        self.trueFalsePage = TrueAndFalseWidget(self)
        # We use the Stack Widget to navigate between different pages
        # If new pages need to be added, import it to this file and add it to the stack
        self.stacked = QStackedWidget()
        self.stacked.addWidget((self.homePage))
        self.stacked.addWidget(self.questionPage)
        self.stacked.addWidget(self.multiplePage)
        self.stacked.addWidget(self.trueFalsePage)
        self.setWindowTitle('Main Window')  # Sets name of window
        # Adds central widget where we are going to do most of our work
        self.setCentralWidget(self.stacked)
        # Sets location (x, y) and size (width, height) of current window
        # self.setGeometry(0, 0, 1600, 900)
        # self.showFullScreen()

        button = QPushButton("text")
        button.setStyleSheet(navigationButtonStyle)
        button.setMinimumHeight(150)
        button.setMaximumWidth(20)
        self.generalLayout.addWidget(button)
    # To navigate to different pages, we set the current widget of the stack
    # These function below are called to nagivate between different pages
    def showQA(self):
        self.stacked.setCurrentWidget(self.questionPage)

    def showMC(self):
        self.stacked.setCurrentWidget(self.multiplePage)

    def showTF(self):
        self.stacked.setCurrentWidget(self.trueFalsePage)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Home()
    win.setStyleSheet(windowStyle)
    win.show()
    sys.exit(app.exec_())
