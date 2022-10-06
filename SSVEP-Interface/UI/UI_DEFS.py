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

STIMULI_SIZE = 260

# Set stimuli frequencies for the main UI
# Note that the key must match the value of the "freqName" passed when creating ButtonContainer object 
MAIN_STIM_FREQUENCIES = { 
    'Enter': 8.25,

    'Output Menu 1': 13.75,
    'Output Menu 2': 10.75,
    'Output Menu 3': 9.75,
    'Output Menu Help': 14.25,

    'Keyboard YN Menu 1': 12.75,
    'Keyboard YN Menu 2': 13.75,
    'Keyboard YN Menu Help': 14.25,
    'Back to Output Menu': 10.75,
    
    'YN 1': 8.75,
    'YN 2': 13.75,

    'Keyboard 1': 12.75,
    'Keyboard 2': 11.75,
    'Keyboard 3': 9.75,
    'Keyboard 4': 10.75,
    'Space': 8.75,
    'Backspace': 13.75,
    'Word Toggle': 14.25,
    }
