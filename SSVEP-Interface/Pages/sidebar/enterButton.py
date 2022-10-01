from PyQt5.QtWidgets import QLabel,QStackedWidget,QLineEdit
from Pages.button_container import ButtonContainer
from server.twitterAPI import tweet

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
# from Pages.BrowserPage.browser import Browser
import sys
from PyQt5.QtWidgets import QApplication

from Pages.HomePage.mainWidgetIndexes import getMainWidgetIndex
from Pages.sidebar.sidebarIndexes import getSidebarIndex

outputMode = ""


class Browser(QWebEngineView):
    def __init__(self, url):
        print("1")
        super().__init__()
        self.loadProgress.connect(print)
        self.load(QUrl(url))
        self.loadFinished.connect(self.pageReady)
        print("2")

    def pageReady(self, success):
        if success:
            self.resize(1600, 900)
            self.show()
        else:
            print('page failed to load')
        print("3")

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
                print("voice not yet implemented")
        elif getOutputMode() == "server":
                print("server not yet implemented")
        elif getOutputMode() == "visual":
                print("displaying visuals...")
                browser = Browser("https://www.craiyon.com/")
                print("visuals displayed")

                # QWebEnginePage.load('http://www.www.pythoncentral.io')
                # QWebEngineView.load('http://www.www.pythoncentral.io')

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

def pageReady(browser, success):
    if success:
        browser.show()
        print("visuals displayed")
    else:
        print("page failed to load")