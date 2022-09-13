from PyQt5.QtWidgets import QLabel,QStackedWidget,QLineEdit
from UI.Components.button_container import ButtonContainer
from server.twitterAPI import tweet

from UI.UI_DEFS import getMainWidgetIndex, MainWidgetIndexes
from UI.BottomWidget.bottomWidgetIndexes import getBottomIndex

from UI.status import setCurrentPage, setOutputMode, printStatus, getPreviousPage

outputMode = ""

class EnterButton(ButtonContainer):
    def __init__(self,parent):
        super().__init__(labelText="Confirm",red=0,blue=0,checkable=False)
        self.clicked.connect(lambda: submitAndReturn(self,parent))

def submitAndReturn(self,parent):
    messageBox = parent.findChild(QLabel,"Prompt")
    mainStack = parent.findChild(QStackedWidget,"Main Widget")
    currWidget = mainStack.currentWidget()
    inputField = parent.findChild(QLineEdit,"Input")

    if currWidget.objectName() == "Output Menu Widget":
        navigateFromOutputMode(parent)
        return
    
    elif currWidget.objectName() == "Selection Menu Widget":
        navigateFromHome(self,parent)
        return

    elif currWidget.objectName() == "Help Widget":
        changeStacks(parent, getMainWidgetIndex(getPreviousPage()), getBottomIndex(getPreviousPage()))

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
    changeStacks(parent,getMainWidgetIndex("home"),getBottomIndex("home"))
    self.label.setText("Confirm")



def navigateFromOutputMode(parent):
    
    labels = ['Twitter','Voice', 'Visual Communication']
    mainButtons = [parent.findChild(ButtonContainer,label) for label in labels]

    for button in mainButtons:
        if button.label.text() == labels[0] and button.isChecked():
            print("going to Twitter")
            setOutputMode("Twitter")
            button.setChecked(False)
            changeStacks(parent,getMainWidgetIndex("home"),getBottomIndex("home"))
        elif button.label.text() == labels[1] and button.isChecked():
            print("going to Voice")
            setOutputMode("Voice")
            button.setChecked(False)
            changeStacks(parent,getMainWidgetIndex("home"),getBottomIndex("home"))
        elif button.label.text() == labels[2] and button.isChecked():
            print("going to Visual Communication")
            setOutputMode("Visual")
            button.setChecked(False)
            changeStacks(parent,getMainWidgetIndex("home"),getBottomIndex("home"))

def navigateFromHome(self,parent):
    
    labels = ['Keyboard', 'Yes/No']
    mainButtons = [parent.findChild(ButtonContainer,label) for label in labels]

    for button in mainButtons:
        if button.label.text() == labels[0] and button.isChecked():
            print("going to Keyboard")
            button.setChecked(False)
            changeStacks(parent,getMainWidgetIndex("keyboard"),getBottomIndex("character only"))
            self.label.setText("Send message")

        elif button.label.text() == labels[1] and button.isChecked():
            print("going to YN")
            button.setChecked(False)
            changeStacks(parent,getMainWidgetIndex("yn"),getBottomIndex("enter only"))
            self.label.setText("Send message")


def changeStacks(parent,mainIndex,bottomIndex):
    mainWidget = parent.findChild(QStackedWidget,"Main Widget")
    bottomWidget = parent.findChild(QStackedWidget,"Bottom Widget")

    mainWidget.setCurrentIndex(mainIndex)
    bottomWidget.setCurrentIndex(bottomIndex)
    setCurrentPage(MainWidgetIndexes[mainIndex])

    printStatus()


def getOutputMode():
    return outputMode