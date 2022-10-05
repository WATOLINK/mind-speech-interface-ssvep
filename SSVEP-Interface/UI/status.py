import os
clear = lambda: os.system('cls')
global i 
i = 1
global status
status = {
    'stimuli': 'on',
    'current page': 'Output Menu Page',
    'previous page': '',
    'output mode': ''
}

def getStimuliStatus():
    global status
    return status['stimuli']

def setStimuliStatus(stimStatus):
    global status
    status['stimuli'] = stimStatus

def getPreviousPage():
    global status
    return status['previous page']

def setPreviousPage(newPreviousPage):
    global status
    status['previous page'] = newPreviousPage

def setCurrentPage(newCurrentPage):
    global status
    setPreviousPage(status['current page'])
    status['current page'] = newCurrentPage
    
def getOutputMode():
    global status
    return status['output mode']

def setOutputMode(newOutputMode):
    global status
    status['output mode'] = newOutputMode

def getStatus():
    global status
    return status

def printStatus():
    # clear()
    global status
    global i
    i += 1
    # print(i)
    # print(' ### PAGE STATUS ###')
    # print(f" Stimuli :       {status['stimuli']}")
    # print(f" Output Mode:    {status['output mode']}")
    # print(f" Previous Page:  {status['previous page']}")
    # print(f" Current Page:   {status['current page']}")
    # print("")
