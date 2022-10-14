import os
from time import time

clear = lambda: os.system('cls')
global i 
i = 1
global status
status = {
    'stimuli': 'on',
    'current page': 'Output Menu Page',
    'output mode': ''
}

def getStimuliStatus():
    global status
    return status['stimuli']

def setStimuliStatus(stimStatus):
    global status
    status['stimuli'] = stimStatus

def setCurrentPage(newCurrentPage):
    global status
    status['current page'] = newCurrentPage
    
def getOutputMode():
    global status
    return status['output mode']

def setOutputMode(newOutputMode):
    global status
    status['output mode'] = newOutputMode

def getStatus():
    global status
    status_update = status
    status_update['timestamp'] = time()
    return status_update

def printStatus():
    global status
    global i
    i += 1