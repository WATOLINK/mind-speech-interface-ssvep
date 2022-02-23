from PyQt5.QtWidgets import QLabel
from Pages.styles import instructionsStyle


def helpWidget():
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
    return instructions
