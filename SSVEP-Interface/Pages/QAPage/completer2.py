from Pages.button_container import ButtonContainer
from PyQt5.QtWidgets import QWidget, QLineEdit



def suggestWords(parent):

    toggleBtn = parent.findChild(ButtonContainer,"Toggle")

    # means the keyboard is currently on word mode
    if toggleBtn.label.text() == "Toggle Characters":
        
        currentText =   parent.findChild(QLineEdit,"Input").text() 

        dummyText = ["among us", "sussy","impostor","ඞ","ඞඞ","ඞඞඞ"]
        dummyText2 = ["crewmate", "tasks","not sussy","fixing lights","medbay scan","check admin"]

        keyboardWidget = parent.findChild(QWidget,"Keyboard Widget")
        keyboardBtns = keyboardWidget.findChildren(ButtonContainer)

        print("Current Text: "+currentText)
        print("in word mode, making some suggestions")

        if keyboardBtns[0].label.text() in dummyText:
            for x in range(len(keyboardBtns)):
                keyboardBtns[x].label.setText(dummyText2[x])
        else:
            for x in range(len(keyboardBtns)):
                keyboardBtns[x].label.setText(dummyText[x])



