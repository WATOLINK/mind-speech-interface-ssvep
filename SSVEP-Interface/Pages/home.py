from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from PyQt5.QtWidgets import (
    QPushButton, QVBoxLayout, QWidget, QLabel
)

from Pages.qa import QuestionAndAnswerWidget
from Pages.search import SearchWidget


class HomeWidget(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        # Creates a verticle template that formats whatever widgets are added to it
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(100, 100, 100, 100)

        # search = self._searchModule()
        # Calls on function to create a center text
        centerText = self._createCenterText()
        # Calls on function to create 3 button
        button1, button2, button3 = self._createNavButtons()

        button1.clicked.connect(parent.showQA)
        button2.clicked.connect(parent.showMC)
        button3.clicked.connect(parent.showTF)

        self.search_widget = SearchWidget(self)
        layout.addWidget(self.search_widget)
        # layout.addWidget(search)
        layout.addWidget(centerText)  # Added components to layout
        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(button3)
        self.setLayout(layout)  # Passing layout to widget

    def _createCenterText(self):
        centertext = QLabel("Home Widget!")
        centertext.setMaximumHeight(100)
        centertext.setFont(QFont('Arial', 32))
        centertext.setAlignment(Qt.AlignCenter)
        return centertext

    def _createNavButtons(self):
        button1 = QPushButton("Page 1")
        button2 = QPushButton("Page 2")
        button3 = QPushButton("Page 3")
        button1.setMinimumHeight(100)
        button2.setMinimumHeight(100)
        button3.setMinimumHeight(100)
        return button1, button2, button3
