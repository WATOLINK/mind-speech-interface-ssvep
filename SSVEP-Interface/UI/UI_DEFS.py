MainWidgetIndexes = [
    "Output Menu Page",
    "Keyboard YN Menu Page",
    "YN Page",
    "Keyboard Page",
    "Help Page"
]

def getMainWidgetIndex(name):
    if name in MainWidgetIndexes:
        return MainWidgetIndexes.index(name)
    else:
        print("invalid sidebar name")

# Set stimuli frequencies for the main UI
# Note that the key must match the value of the "freqName" passed when creating ButtonContainer object 
MAIN_STIM_FREQUENCIES = { 
    'Enter': 1,

    'Output Menu 1': 1,
    'Output Menu 2': 1,
    'Output Menu 3': 1,
    'Output Menu Help': 1,

    'Keyboard YN Menu 1': 1,
    'Keyboard YN Menu 2': 1,
    'Keyboard YN Menu Help': 1,
    'Back to Output Menu': 1,
    
    'YN 1': 1,
    'YN 2': 1,

    'Keyboard 1': 1,
    'Keyboard 2': 1,
    'Keyboard 3': 1,
    'Keyboard 4': 1,
    'Space': 1,
    'Backspace': 1,
    'Word Toggle': 1,
    }
