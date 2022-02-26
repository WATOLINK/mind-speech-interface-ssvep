import sys
from PyQt5.QtCore import center, Qt
from PyQt5.QtGui import QFont

from PyQt5.QtWidgets import QApplication, QStackedWidget, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtWidgets import QMainWindow

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

         # Make sure to pass in 'self' to the child widget for it to access parent to for methods and children
        self.homePage = HomePageWidget(self)

        self.setWindowTitle('Main Window')  # Sets name of window
        # Adds central widget where we are going to do most of our work
        self.setCentralWidget(self.homePage)
        self.setGeometry(0, 0, 1600, 900)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Home()
    win.setStyleSheet(windowStyle)
    win.show()
    sys.exit(app.exec_())
