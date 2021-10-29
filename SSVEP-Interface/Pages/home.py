from PyQt5.QtCore import  Qt
from PyQt5.QtGui import QFont

from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget
from PyQt5.QtWidgets import QLabel

from Pages.qa import QuestionAndAnswerWidget

class HomeWidget(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        
        layout = QVBoxLayout() # Creates a verticle template that formats whatever widgets are added to it
        layout.setSpacing(0)
        layout.setContentsMargins(100, 100, 100, 100)    

        centerText = self._createCenterText() # Calls on function to create a center text
        button1, button2, button3 = self._createNavButtons() # Calls on function to create 3 button

        button1.clicked.connect(parent.showQA)
        button2.clicked.connect(parent.showMC)
        button3.clicked.connect(parent.showTF)
        
        layout.addWidget(centerText) # Added components to layout
        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(button3)

        self.setLayout(layout) # Passing layout to widget

    
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