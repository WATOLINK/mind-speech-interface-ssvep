import sys
from PyQt5.QtWidgets import QApplication, QButtonGroup, QWidget, QGridLayout, QLineEdit, QLabel, QPushButton, QStackedWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore

from UI.styles import textBoxStyle, sideBarStyle, mainButtonStyle, promptBoxStyle, instructionsStyle
from UI.Components.button_container import ButtonContainer
from UI.YNPage.YN import YesNoWidget
from UI.KeyboardPage.keyboard2 import KeyboardWidget
from UI.HelpPage.help import HelpWidget
from UI.BottomWidget.bottomWidget import BottomWidget
from UI.KeyboardPage.completer2 import suggestWords

from UI.Components.enterButton import EnterButton

from UI.UI_DEFS import MainWidgetIndexes
from UI.BottomWidget.bottomWidgetIndexes import getBottomIndex

from UI.status import setCurrentPage, printStatus

def disableOtherButtons(buttons, selected):
    
    if selected.isChecked():
        # title.setText(selected.label.text())
        for button in buttons:
            if button != selected:
                button.setChecked(False)
    # else:
        # title.setText("")

def changeStacks(parent,mainIndex,sidebarIndex):
    mainStack = parent.findChild(QStackedWidget,"Main Widget")
    bottomStack = parent.findChild(QStackedWidget,"Bottom Widget")

    mainStack.setCurrentIndex(mainIndex)
    bottomStack.setCurrentIndex(sidebarIndex)
    setCurrentPage(MainWidgetIndexes[mainIndex])

    printStatus()