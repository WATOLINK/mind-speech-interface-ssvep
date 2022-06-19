from PyQt5 import QtWidgets
from PyQt5 import QtCore


from Pages.styles import promptBoxStyle
from Pages.button_container import ButtonContainer

from Pages.HomePage.homepage import promptBox, inputBox
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit

class YesNoWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        
        layout = self.createLayout(parent)
        self.setObjectName("YN Widget")
        self.setLayout(layout)

    #Create Yes and no buttons and their functions
    def createLayout(self,parent):
        layout = QHBoxLayout()
        labels = ["Yes", "No"]
        buttons = []

        for i in range(len(labels)):
            button = ButtonContainer(labels[i])
            button.setObjectName(labels[i])
            layout.addWidget(button)
            buttons.append(button)

        buttons[0].clicked.connect(lambda: disableOtherButtons(parent, buttons, buttons[0]))
        buttons[1].clicked.connect(lambda: disableOtherButtons(parent, buttons, buttons[1]))

        return layout

# make the yn array of buttons single select + display selection input field
def disableOtherButtons(parent,buttons, selected):    

    inputField = parent.findChild(QLineEdit,"Input")

    if selected.isChecked():
        
        inputField.setText(selected.objectName())

        for button in buttons:
            if button != selected:
                button.setChecked(False)    
    else:
        inputField.clear()
