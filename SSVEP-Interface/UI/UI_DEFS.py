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

WINDOW_WIDTH = 2400
WINDOW_HEIGHT = 1360

STIMULI_SIZE = 120

# Set stimuli frequencies for the main UI
# Note that the key must match the value of the "freqName" passed when creating ButtonContainer object 
MAIN_STIM_FREQUENCIES = { 
    'Enter': 13.25,

    'Output Menu 1': 11.75,
    'Output Menu 2': 10.25,
    'Output Menu 3': 9.25,
    'Output Menu Help': 12.75,

    'Keyboard YN Menu 1': 12.75,
    'Keyboard YN Menu 2': 14.75,
    'Keyboard YN Menu Help': 9.25,
    'Back to Output Menu': 10.75,
    
    'YN 1': 10.25,
    'YN 2': 14.75,

    'Keyboard 1': 12.75,
    'Keyboard 2': 11.75,
    'Keyboard 3': 9.25,
    'Keyboard 4': 10.75,
    'Space': 11.25,
    'Backspace': 10.25,
    'Word Toggle': 14.75,
    }
