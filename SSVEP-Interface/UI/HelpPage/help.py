from PyQt5.QtWidgets import QLabel,QWidget,QHBoxLayout
from UI.styles import instructionsStyle

class HelpWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName("Help Widget")
        layout = self.createLayout(parent)
        self.setLayout(layout)


    def createLayout(self,parent):
        layout = QHBoxLayout()
        instructions = QLabel("""Instructions:

        Home Page
        - Select mode of text entry
        - Select “Enter” to confirm your selection 

        Yes/No and Multiple Choice
        - Select choice of response
        - To change choice, select a different option
        - Select “Enter” to confirm your selection

        Typing 
        - Words/Sentences: Select AI recommended words and phrases to complete your response
        - Grouped Characters: Select groupings of characters to choose individual characters
        - Individual Characters: Select individual characters to submit custom text""")
        instructions.setStyleSheet(instructionsStyle)
        layout.addWidget(instructions)
        return layout