MainWidgetIndexes = [
    "output mode",
    "home",
    "mc",
    "yn",
    "keyboard",
    "help"
]

def getMainWidgetIndex(name):
    if name in MainWidgetIndexes:
        return MainWidgetIndexes.index(name)
    else:
        print("invalid sidebar name")