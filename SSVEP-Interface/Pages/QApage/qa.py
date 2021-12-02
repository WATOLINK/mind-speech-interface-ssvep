
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QWidget

from Pages.QAPage.keyboard import KeyboardInput


class QuestionAndAnswerWidget(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        layout = self._createLayout(parent)
        self.setLayout(layout)

    # Method creates the layout of the page, called in the init function to maintain clean and readable code
    # If you are changing the functionalities of the page, you will most likely want to alter this method
    def _createLayout(self, parent):
        # Creates a verticle template that formats whatever widgets are added to it
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(100, 100, 100, 100)
        centerWidget = KeyboardInput()
        button2 = self._createBackButton(text=">")
        button2.clicked.connect(parent.showTF)
        layout.addWidget(centerWidget)
        layout.addWidget(button2)
        layout.setAlignment(Qt.AlignVCenter)
        return layout

    def _createBackButton(self, text):
        button = QPushButton(text)
        button.setMinimumHeight(150)
        button.setMaximumWidth(20)
        return button
