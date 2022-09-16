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
    'Enter': 10,

    'Output Menu 1': 10,
    'Output Menu 2': 10,
    'Output Menu 3': 10,
    'Output Menu Help': 10,

    'Keyboard YN Menu 1': 10,
    'Keyboard YN Menu 2': 10,
    'Keyboard YN Menu Help': 10,
    'Back to Output Menu': 10,
    
    'YN 1': 10,
    'YN 2': 10,

    'Keyboard 1': 10,
    'Keyboard 2': 10,
    'Keyboard 3': 10,
    'Keyboard 4': 10,
    'Space': 10,
    'Backspace': 10,
    'Word Toggle': 10,
    }
