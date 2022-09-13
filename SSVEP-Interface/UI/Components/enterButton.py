from PyQt5.QtWidgets import QLabel,QStackedWidget,QLineEdit
from UI.Components.button_container import ButtonContainer
from server.twitterAPI import tweet

from UI.UI_DEFS import getMainWidgetIndex, MainWidgetIndexes

from UI.status import setOutputMode, getPreviousPage

from UI.helperFunctions import disableOtherButtons, changeStacks\

outputMode = ""

class EnterButton(ButtonContainer):
    def __init__(self,parent):
        super().__init__(labelText="Confirm",freqName="Enter",checkable=False)
        self.clicked.connect(lambda: submitAndReturn(self,parent))

def submitAndReturn(self,parent):
    messageBox = parent.findChild(QLabel,"Prompt")
    mainStack = parent.findChild(QStackedWidget,"Main Widget")
    currWidget = mainStack.currentWidget()
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
        if getOutputMode() == "twitter":
                print("tweeting")
                tweet(inputField.text())
        elif getOutputMode() == "voice":
                print("voice not yet implemented")
        elif getOutputMode() == "visual":
                print("visual not yet implemented")

        inputField.clear()

    # uncheck any checked boxes on submission
    for button in currWidget.findChildren(ButtonContainer):
        if button.isChecked():
            button.setChecked(False)

    # Go back to main page
    changeStacks(parent,getMainWidgetIndex("Keyboard YN Menu Page"))
    self.label.setText("Confirm")



def navigateFromOutputMode(parent):
    
    labels = ['Twitter','Voice', 'Visual Communication']
    mainButtons = [parent.findChild(ButtonContainer,label) for label in labels]

    for button in mainButtons:
        if button.label.text() == labels[0] and button.isChecked():
            print("going to Twitter")
            setOutputMode("Twitter")
            button.setChecked(False)
            changeStacks(parent,getMainWidgetIndex("Keyboard YN Menu Page"))
        elif button.label.text() == labels[1] and button.isChecked():
            print("going to Voice")
            setOutputMode("Voice")
            button.setChecked(False)
            changeStacks(parent,getMainWidgetIndex("Keyboard YN Menu Page"))
        elif button.label.text() == labels[2] and button.isChecked():
            print("going to Visual Communication")
            setOutputMode("Visual")
            button.setChecked(False)
            changeStacks(parent,getMainWidgetIndex("Keyboard YN Menu Page"))

def navigateFromHome(self,parent):
    
    labels = ['Keyboard', 'Yes/No']
    mainButtons = [parent.findChild(ButtonContainer,label) for label in labels]

    for button in mainButtons:
        if button.label.text() == labels[0] and button.isChecked():
            print("going to Keyboard")
            button.setChecked(False)
            changeStacks(parent,getMainWidgetIndex("Keyboard Page"))
            self.label.setText("Send message")

        elif button.label.text() == labels[1] and button.isChecked():
            print("going to YN")
            button.setChecked(False)
            changeStacks(parent,getMainWidgetIndex("YN Page"))
            self.label.setText("Send message")



def getOutputMode():
    return outputMode