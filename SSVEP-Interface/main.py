import sys
from PyQt5.QtCore import center, Qt
from PyQt5.QtGui import QFont

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow

from Pages.home import HomeWidget
from Pages.qa import QuestionAndAnswerWidget
from Pages.mc import MultipleChoiceWidget
from Pages.absolute import TrueAndFalseWidget

class Window(QMainWindow):
    """Main Window."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)

        self.home = HomeWidget(self)

        self.setWindowTitle('Main Window') # Sets name of window
        self.setCentralWidget(self.home) # Adds central widget where we are going to do most of our work
        self.setGeometry(0, 0, 1600, 900) # Sets location (x, y) and size (width, height) of current window

    def back(self):
        self.home = HomeWidget(self)
        self.setCentralWidget(self.home)
    
    def showQA(self):
        self.first = QuestionAndAnswerWidget(self)
        self.setCentralWidget(self.first)

    def showMC(self):
        self.second = MultipleChoiceWidget(self)
        self.setCentralWidget(self.second)

    def showTF(self):
        self.third = TrueAndFalseWidget(self)
        self.setCentralWidget(self.third)

    # Functions below may be useful int he future
    # def _createMenu(self):
    #     self.menu = self.menuBar().addMenu("&Menu")
    #     self.menu.addAction('&Exit', self.close)

    # def _createToolBar(self):
    #     tools = QToolBar()
    #     self.addToolBar(tools)
    #     tools.addAction('Exit', self.close)

    # def _createStatusBar(self):
    #     status = QStatusBar()
    #     status.showMessage("I'm the Status Bar")
    #     self.setStatusBar(status)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())