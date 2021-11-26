from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QButtonGroup, QGridLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QVBoxLayout, QWidget
from Pages.styles import toggleButtonStyle, confirmButtonStyle, navigationButtonStyle


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

        button1 = self._createBackButton(text="←")
        button1.clicked.connect(parent.showTF)

        centralLayout = self._createCentralLayout()

        buttonLayout = self._createButtonLayout()
        confirmButton = self._createConfirmButton()
        self.previewText = self._createPreviewText()

        centralLayout.addWidget(self.previewText, alignment=Qt.AlignCenter)
        centralLayout.addLayout(buttonLayout)
        centralLayout.addWidget(confirmButton, alignment=Qt.AlignCenter)

        layout.addWidget(button1)
        layout.addLayout(centralLayout)
        layout.setAlignment(Qt.AlignVCenter)

        return layout


    def _createCentralLayout(self):
        centralLayout = QVBoxLayout()
        return centralLayout


    def _createButtonLayout(self):
        self.buttonGroup = QButtonGroup()
        buttonLayout = QGridLayout()
        buttons = {'A': (0, 0), 'B': (0, 1), 'C': (0, 2),
                    'D': (1,0), 'E': (1,1), 'F': (1,2)}
        
        for buttonText, pos in buttons.items():
            button = QPushButton(buttonText)
            button.setCheckable(True)
            button.setStyleSheet(toggleButtonStyle)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            buttonLayout.addWidget(button, pos[0], pos[1])
            self.buttonGroup.addButton(button)
            
        return buttonLayout


    # Confirm selection callback
    def _handleConfirm(self):
        if self.buttonGroup.checkedButton():
            self.previewText.setText(self.buttonGroup.checkedButton().text())


    def _createConfirmButton(self):
        confirmButton = QPushButton("Confirm")
        confirmButton.setStyleSheet(confirmButtonStyle)
        confirmButton.clicked.connect(self._handleConfirm)
        return confirmButton


    def _createPreviewText(self):
        previewText = QLabel()
        previewText.setFont(QFont('Arial', 32))
        return previewText
    
    
    def _createBackButton(self, text):
        button = QPushButton(text)
        button.setStyleSheet(navigationButtonStyle)
        return button