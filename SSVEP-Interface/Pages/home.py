from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget, QGridLayout

from Pages.search import SearchWidget


# This page is not part of the finished application, just a place to put WIP items that does not yet have a place on other pages
class HomeWidget(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        layout = self._createLayout(parent)
        self.setLayout(layout)

    # Method creates the layout of the page, called in the init function to maintain clean and readable code
    # If you are changing the functionalities of the page, you will most likely want to alter this method
    def _createLayout(self, parent):
        # Creates a verticle template that formats whatever widgets are added to it
        # layout = QHBoxLayout()

        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(100, 100, 100, 100)
        centerText = self._createCenterText()
        button1 = self._createBackButton(text=">")
        button1.clicked.connect(parent.showQA)

        searchWidget = SearchWidget()

        layout.addWidget(centerText, 0, 0)
        layout.addWidget(searchWidget, 1, 0)
        layout.addWidget(button1, 0, 1, 1, 1)
        layout.setAlignment(Qt.AlignVCenter)
        layout.setSpacing(5)
        return layout

    def _createCenterText(self):
        centertext = QLabel("Home Page, Add Search Widget here")
        centertext.setMaximumHeight(100)
        centertext.setFont(QFont('Arial', 20))
        centertext.setAlignment(Qt.AlignCenter)
        return centertext

    def _createBackButton(self, text):
        button = QPushButton(text)
        button.setMinimumHeight(150)
        button.setMaximumWidth(20)
        return button
