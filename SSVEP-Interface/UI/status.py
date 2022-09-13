import os
clear = lambda: os.system('cls')


previousPage = ""
currentPage = "output menu"
outputMode = "" 

def getPreviousPage():
    return previousPage

def getCurrentPage():
    return currentPage

def setCurrentPage(newCurrentPage):
    global previousPage 
    global currentPage

    previousPage = currentPage
    currentPage = newCurrentPage
    
    
def getOutputMode():
    return outputMode

def setOutputMode(newOutputMode):
    global outputMode
    outputMode = newOutputMode

def printStatus():
    # clear()
    print(" ### PAGE STATUS ###")
    print(f" Previous Page: {previousPage}")
    print(f" Current Page: {currentPage}")
    print(f" Output Mode: {outputMode}")
    print(" ###################")
