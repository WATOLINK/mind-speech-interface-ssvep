"""UI Page Frequencies"""
MAIN_WIDGET_INDEXES = [
    "Output Menu Page",
    "Keyboard YN Menu Page",
    "YN Page",
    "Keyboard Page",
    "Help Page"
]

def getMainWidgetIndex(name):
    if name in MAIN_WIDGET_INDEXES:
        return MAIN_WIDGET_INDEXES.index(name)
    else:
        print("invalid sidebar name")

#WINDOW_WIDTH = 1900
#WINDOW_HEIGHT = 1061

WINDOW_WIDTH = 2400
WINDOW_HEIGHT = 1360

STIMULI_SIZE = 200

# Set stimuli frequencies for the main UI
# Note that the key must match the value of the "freqName" passed when creating ButtonContainer object 
MAIN_STIM_FREQUENCIES = {
    'Enter': 8.25,

    'Output Menu 1': 10.75,
    'Output Menu 2': 13.75,
    'Output Menu Help': 14.25,

    'Keyboard YN Menu 1': 12.75,
    'Keyboard YN Menu 2': 13.75,
    'Back to Output Menu': 10.75,
    
    'YN 1': 8.75,
    'YN 2': 9.75,

    'Keyboard 1': 12.75,
    'Keyboard 2': 11.75,
    'Keyboard 3': 14.25,
    'Keyboard 4': 9.75,
    'Space': 8.75,
    'Backspace': 10.75,
    'Word Toggle': 13.75,
}

START_DELAY = 5

PAGE_STIM_ONSET_TIMES = {
    'Output Menu Page': 5,
    'Keyboard YN Menu Page': 5,
    'YN Page': 5,
    'Keyboard Page': 5,
    'Help Page': 5,
}