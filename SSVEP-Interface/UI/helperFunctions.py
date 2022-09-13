from PyQt5.QtWidgets import QStackedWidget

from UI.UI_DEFS import MainWidgetIndexes

from UI.status import setCurrentPage, printStatus

def disableOtherButtons(buttons, selected):
    
    if selected.isChecked():
        # title.setText(selected.label.text())
        for button in buttons:
            if button != selected:
                button.setChecked(False)
    # else:
        # title.setText("")

def changeStacks(parent,mainIndex):
    mainStack = parent.findChild(QStackedWidget,"Main Widget")
    # bottomStack = parent.findChild(QStackedWidget,"Bottom Widget")

    mainStack.setCurrentIndex(mainIndex)
    # bottomStack.setCurrentIndex(sidebarIndex)
    setCurrentPage(mainStack.currentWidget().objectName())

    printStatus(parent)