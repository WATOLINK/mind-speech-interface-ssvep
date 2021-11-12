from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget


class MultipleChoiceWidget(QWidget):

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
        centerText = self._createCenterText()
        button1 = self._createBackButton(text="<")
        button1.clicked.connect(parent.showTF)
        layout.addWidget(button1)
        layout.addWidget(centerText)
        layout.setAlignment(Qt.AlignVCenter)
        return layout


    def _createCenterText(self):
        centertext = QLabel("Multiple Choice Page!")
        centertext.setMaximumHeight(100)
        centertext.setFont(QFont('Arial', 32))
        centertext.setAlignment(Qt.AlignCenter)
        return centertext
    
    
    def _createBackButton(self, text):
        button = QPushButton(text)
        button.setMinimumHeight(150)
        button.setMaximumWidth(20)
        return button