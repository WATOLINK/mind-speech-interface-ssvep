from PyQt5.QtWidgets import QLabel,QStackedWidget,QLineEdit
from Pages.button_container import ButtonContainer
from server.twitterAPI import tweet

from Pages.HomePage.mainWidgetIndexes import getMainWidgetIndex
from Pages.sidebar.sidebarIndexes import getSidebarIndex
from _TTS.watolink_TTS import *

outputMode = ""
TTS = TTS_synthesizer(model_name = "tts_models/en/ljspeech/tacotron2-DDC")

class EnterButton(ButtonContainer):
    def __init__(self,parent):
        super().__init__(labelText="Enter",red=0,blue=0,checkable=False)
        self.clicked.connect(lambda: submitAndReturn(parent))

def submitAndReturn(parent):
    messageBox = parent.findChild(QLabel,"Prompt")
    mainStack = parent.findChild(QStackedWidget,"Main Stack")
    currWidget = mainStack.currentWidget()
    inputField = parent.findChild(QLineEdit,"Input")

    if inputField.text():
        temp = messageBox.text() + f"[{inputField.text()}]"
        messageBox.setText(temp)
        if getOutputMode() == "twitter":
                print("tweeting")
                tweet(inputField.text())
        elif getOutputMode() == "voice":
                print("voice not yet implemented. Input field text:", inputField.text())
                # Convert input text to speech (TTS)
                TTS.synthesize(text = inputField.text())
        elif getOutputMode() == "server":
                print("server not yet implemented")
        elif getOutputMode() == "visual":
                print("visual not yet implemented")

        inputField.clear()

    if currWidget.objectName() == "MC Widget" or currWidget.objectName() == "YN Widget":
        # uncheck any checked boxes on submission
        for button in currWidget.findChildren(ButtonContainer):
            if button.isChecked():
                button.setChecked(False)

    # Go back to main page
    changeStacks(parent,getMainWidgetIndex("home"),getSidebarIndex("home"))

def changeStacks(parent,mainIndex,sidebarIndex):
    mainStack = parent.findChild(QStackedWidget,"Main Stack")
    sidebarStack = parent.findChild(QStackedWidget,"Sidebar Stack")

    mainStack.setCurrentIndex(mainIndex)
    sidebarStack.setCurrentIndex(sidebarIndex)

def getOutputMode():
    return outputMode
