
MAIN_WIDGET_INDEXES = [
    "Output Menu Page",
    "Keyboard YN Menu Page",
    "YN Page",
    "Keyboard Page",
    "Help Page"
]

MAIN_STIM_FREQUENCIES = {
    'Enter': 8.25,

    'Output Menu 1': 10.75,
    'Output Menu 2': 11.75,
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

MAIN_WIDGET_INDEXES = [
    "Output Menu Page",
    "Keyboard YN Menu Page",
    "YN Page",
    "Keyboard Page",
    "Help Page"
]


page_frequencies = {
    page_name: [freq for name, freq in MAIN_STIM_FREQUENCIES.items() if ' '.join(name.split()[:-1]) in page_name]
    for page_name in MAIN_WIDGET_INDEXES
}

