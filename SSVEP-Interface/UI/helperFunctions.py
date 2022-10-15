from PyQt5.QtWidgets import QStackedWidget
from UI.Components.button_container import buttonClickNoise

from UI.status import setCurrentPage, printStatus

def disableOtherButtons(buttons, selected):
    # buttonClickNoise()
    
    if selected.isChecked():
        for button in buttons:
            if button != selected:
                button.setChecked(False)

def changeStacks(parent, mainIndex):
    buttonClickNoise()

    mainStack = parent.findChild(QStackedWidget,"Main Widget")

    mainStack.setCurrentIndex(mainIndex)
    setCurrentPage(mainStack.currentWidget().objectName())
