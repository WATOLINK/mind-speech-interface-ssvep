from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget


class MultipleChoiceWidget(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        layout = QVBoxLayout() # Creates a verticle template that formats whatever widgets are added to it
        layout.setSpacing(0)
        layout.setContentsMargins(100, 100, 100, 100)    

        centerText = self._createCenterText()
        button = self._createBackButton()

        button.clicked.connect(parent.back)

        layout.addWidget(button)
        layout.addWidget(centerText)

        layout.setAlignment(Qt.AlignTop)
        
        self.setLayout(layout)

    def _createCenterText(self):
        centertext = QLabel("Multiple Choice Page!")
        centertext.setMaximumHeight(100)
        centertext.setFont(QFont('Arial', 32))
        centertext.setAlignment(Qt.AlignCenter)
        return centertext
    
    def _createBackButton(self):
        button = QPushButton("Back")
        button.setMinimumHeight(20)
        button.setMaximumWidth(50)
        return button