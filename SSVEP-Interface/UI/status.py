import os
clear = lambda: os.system('cls')
from PyQt5.QtWidgets import QStackedWidget


outputMode = "" 
previousPage = ""
currentPage = "Output Menu Page"


def getPreviousPage():
    return previousPage

def setPreviousPage(newPreviousPage):
    global previousPage
    previousPage = newPreviousPage

def setCurrentPage(newCurrentPage):
    global currentPage

    setPreviousPage(currentPage)
    currentPage = newCurrentPage
    
def getOutputMode():
    return outputMode

def setOutputMode(newOutputMode):
    global outputMode
    outputMode = newOutputMode

def printStatus(parent):
    # clear()
    print(" ### PAGE STATUS ###")
    print(f" Output Mode:    {outputMode}")
    print(f" Previous Page:  {previousPage}")
    mainStack = parent.findChild(QStackedWidget,"Main Widget")
    print(f" Current Page:   {mainStack.currentWidget().objectName()}")
    print(" ###################")
