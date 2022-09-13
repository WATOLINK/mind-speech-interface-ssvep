BottomIndexes = [
    "output menu",
    "home",
    "character only",
    "enter only",
    "enter only return to output menu"
]

def getBottomIndex(name):
    if name in BottomIndexes:
        return BottomIndexes.index(name)
    else:
        print("invalid bottom widget name")