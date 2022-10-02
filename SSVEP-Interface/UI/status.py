import os
clear = lambda: os.system('cls')

status = {
    'stimuli': 'on',
    'current page': 'Output Menu Page',
    'previous page': '',
    'output mode': '',
}

def getStimuliStatus():
    return status['stimuli']

def setStimuliStatus(stimStatus):
    status['stimuli'] = stimStatus

def getPreviousPage():
    return status['previous page']

def setPreviousPage(newPreviousPage):
    status['previous page'] = newPreviousPage

def setCurrentPage(newCurrentPage):
    setPreviousPage(status['current page'])
    status['current page'] = newCurrentPage
    
def getOutputMode():
    return status['output mode']

def setOutputMode(newOutputMode):
    status['output mode'] = newOutputMode

def printStatus():
    clear()
    print(' ### PAGE STATUS ###')
    print(f" Stimuli :       {status['stimuli']}")
    print(f" Output Mode:    {status['output mode']}")
    print(f" Previous Page:  {status['previous page']}")
    print(f" Current Page:   {status['current page']}")
    print("")
