from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit

from UI.Components.button_container import ButtonContainer# buttonClickNoise

from gtts import gTTS
from playsound import playsound

import os


class YesNoWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        layout = self.createLayout(parent)
        self.setObjectName("YN Page")
        self.setLayout(layout)


    def createLayout(self,parent):
        layout = QHBoxLayout()
        labels = ["Yes", "No"]
        buttons = []

        for i in range(len(labels)):
            button = ButtonContainer(labels[i], freqName=f"YN {i+1}")
            button.setObjectName(labels[i])
            layout.addWidget(button)
            buttons.append(button)

        buttons[0].clicked.connect(lambda: yesNoVoice(parent, buttons, buttons[0], "Yes"))
        buttons[1].clicked.connect(lambda: yesNoVoice(parent, buttons, buttons[1], "No"))

        return layout

def TTS (text):
    myobj = gTTS(text=text, lang='en', slow=False)

    #myobj.save("yesno.mp3")
    #playsound("yesno.mp3")

def yesNoVoice(parent,buttons, selected, text):
    disableOtherButtonsYN(parent,buttons,selected)
    TTS(text)

# make the yn array of buttons single select + display selection input field
def disableOtherButtonsYN(parent,buttons, selected):    
    #buttonClickNoise()

    inputField = parent.findChild(QLineEdit,"Input")

    if selected.isChecked():
        
        inputField.setText(selected.objectName())

        for button in buttons:
            if button != selected:
                button.setChecked(False)    
    else:
        inputField.clear()