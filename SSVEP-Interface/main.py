import sys
from PyQt5.QtCore import center, Qt
from PyQt5.QtGui import QFont

from PyQt5.QtWidgets import QApplication, QStackedWidget
from PyQt5.QtWidgets import QMainWindow

from Pages.qa import QuestionAndAnswerWidget
from Pages.mc import MultipleChoiceWidget
from Pages.absolute import TrueAndFalseWidget
from Pages.search import SearchWidget


class Window(QMainWindow):
    """Main Window."""

    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        # Make sure to pass in 'self' to the child widget for it to access parent methods
        self.multiplePage = MultipleChoiceWidget(self)
        self.questionPage = QuestionAndAnswerWidget(self)
        self.trueFalsePage = TrueAndFalseWidget(self)
        self.search_widget = SearchWidget(self)
        # We use the Stack Widget to navigate between different pages
        # If new pages need to be added, import it to this file and add it to the stack
        self.stacked = QStackedWidget()
        self.stacked.addWidget(self.search_widget)
        self.stacked.addWidget(self.questionPage)
        self.stacked.addWidget(self.multiplePage)
        self.stacked.addWidget(self.trueFalsePage)
        self.setWindowTitle('Main Window')  # Sets name of window
        # Adds central widget where we are going to do most of our work
        self.setCentralWidget(self.stacked)
        # Sets location (x, y) and size (width, height) of current window
        self.setGeometry(0, 0, 1600, 900)

    # To navigate to different pages, we set the current widget of the stack
    # These function below are called to nagivate between different pages
    def showQA(self):
        self.stacked.setCurrentWidget(self.questionPage)

    def showMC(self):
        self.stacked.setCurrentWidget(self.multiplePage)

    def showTF(self):
        self.stacked.setCurrentWidget(self.trueFalsePage)

    # Functions below may be useful in the future
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
