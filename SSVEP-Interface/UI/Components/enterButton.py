from PyQt5.QtWidgets import QLabel,QStackedWidget,QLineEdit
from UI.Components.button_container import ButtonContainer
from server.twitterAPI import tweet
# from _TTS.watolink_TTS import *

from playsound import playsound


from UI.UI_DEFS import getMainWidgetIndex

from UI.status import setOutputMode, getPreviousPage, getOutputMode

from UI.helperFunctions import disableOtherButtons, changeStacks

# TTS = TTS_synthesizer(model_name = "tts_models/en/ljspeech/tacotron2-DDC")

class EnterButton(ButtonContainer):
    def __init__(self,parent):
        super().__init__(labelText="Confirm",freqName="Enter",checkable=False)
        self.setObjectName("Enter Button")
        self.clicked.connect(lambda: submitAndReturn(self,parent))

def submitAndReturn(self,parent):
    messageBox = parent.findChild(QLabel,"Prompt")
    mainStack = parent.findChild(QStackedWidget,"Main Widget")
    currWidget = mainStack.currentWidget()
    print(currWidget)
    inputField = parent.findChild(QLineEdit,"Input")

    if currWidget.objectName() == "Output Menu Page":
        navigateFromOutputMode(parent)
        return
    
    elif currWidget.objectName() == "Keyboard YN Menu Page":
        navigateFromHome(self,parent)
        return

    elif currWidget.objectName() == "Help Page":
        changeStacks(parent, getMainWidgetIndex(getPreviousPage()))
        return

    if inputField.text():
        temp = messageBox.text() + f"[{inputField.text()}]"
        messageBox.setText(temp)
        if getOutputMode() == "Twitter":
                print("tweeting")
                tweet(inputField.text())
        elif getOutputMode() == "Voice":
                print("voice not yet implemented")
                # TTS.synthesize(text = inputField.text())

        inputField.clear()

    # uncheck any checked boxes on submission
    for button in currWidget.findChildren(ButtonContainer):
        if button.isChecked():
            button.setChecked(False)

    # Go back to main page
    changeStacks(parent,getMainWidgetIndex("Keyboard YN Menu Page"))
    self.label.setText("Confirm")



def navigateFromOutputMode(parent):
    
    labels = ['Use Twitter','Use Voice']
    mainButtons = [parent.findChild(ButtonContainer,label) for label in labels]

    print("clicked")

    for button in mainButtons:
        if button.isChecked():
            if button.label.text() == labels[0]:
                # print("going to Twitter")
                setOutputMode("Twitter")
            elif button.label.text() == labels[1]:
                # print("going to Voice")
                setOutputMode("Voice")

            button.setChecked(False)
            changeStacks(parent,getMainWidgetIndex("Keyboard YN Menu Page"))
        

def navigateFromHome(self,parent):
    
    labels = ['Use Keyboard', 'Use Yes/No']
    mainButtons = [parent.findChild(ButtonContainer,label) for label in labels]

    for button in mainButtons:
        if button.label.text() == labels[0] and button.isChecked():
            # print("going to Keyboard")
            button.setChecked(False)
            changeStacks(parent,getMainWidgetIndex("Keyboard Page"))
            self.label.setText("Send message")

        elif button.label.text() == labels[1] and button.isChecked():
            # print("going to YN")
            button.setChecked(False)
            changeStacks(parent,getMainWidgetIndex("YN Page"))
            self.label.setText("Send message")
