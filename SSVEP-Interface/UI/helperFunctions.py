from PyQt5.QtWidgets import QStackedWidget
from UI.Components.button_container import buttonClickNoise

from UI.status import setCurrentPage, printStatus

def disableOtherButtons(buttons, selected):
    # buttonClickNoise()
    print(selected)
    print("")
    print("")
    if selected.isChecked():
        # title.setText(selected.label.text())
        for button in buttons:
            if button != selected:
                button.setChecked(False)
    # else:
        # title.setText("")

def changeStacks(parent, mainIndex):
    # buttonClickNoise()

    mainStack = parent.findChild(QStackedWidget,"Main Widget")
    # bottomStack = parent.findChild(QStackedWidget,"Bottom Widget")

    mainStack.setCurrentIndex(mainIndex)
    # bottomStack.setCurrentIndex(sidebarIndex)
    setCurrentPage(mainStack.currentWidget().objectName())

    # printStatus(parent)