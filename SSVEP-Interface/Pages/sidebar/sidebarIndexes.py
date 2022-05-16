SidebarIndexes = [
    "output mode",
    "home",
    "character only",
    "enter only",
    "enter only return to output mode"
]

def getSidebarIndex(name):
    if name in SidebarIndexes:
        return SidebarIndexes.index(name)
    else:
        print("invalid sidebar name")