from PyQt5.QtWidgets import QLabel,QStackedWidget,QLineEdit
from Pages.button_container import ButtonContainer
from server.twitterAPI import tweet, isTweeting

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
        if isTweeting():
            tweet(inputField.text())

        inputField.clear()

    if currWidget.objectName() == "MC Widget" or currWidget.objectName() == "YN Widget":
        # uncheck any checked boxes on submission
        for button in currWidget.findChildren(ButtonContainer):
            if button.isChecked():
                button.setChecked(False)

    # Go back to main page
    changeStacks(parent,1,1)

def changeStacks(parent,mainIndex,sidebarIndex):
    mainStack = parent.findChild(QStackedWidget,"Main Stack")
    sidebarStack = parent.findChild(QStackedWidget,"Sidebar Stack")

    mainStack.setCurrentIndex(mainIndex)
    sidebarStack.setCurrentIndex(sidebarIndex)