from PyQt5.QtWidgets import QWidget, QGridLayout,QLineEdit
from PyQt5 import QtCore

from Pages.button_container import ButtonContainer


class MultipleChoiceWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        layout = self.createLayout(parent)
        self.setObjectName("MC Widget")
        self.setLayout(layout)


    def createLayout(self,parent):
        layout = QGridLayout()
        labels = [["A", "B"], ["C", "D"]]

        buttons=[]

        for row in range(len(labels)):
            for col in range(len(labels[0])):
                button = ButtonContainer(labels[row][col])
                button.setObjectName(labels[row][col])
                layout.addWidget(button, row, col)
                buttons.append(button)


        buttons[0].clicked.connect(lambda: disableOtherButtons(parent,buttons, buttons[0]))
        buttons[1].clicked.connect(lambda: disableOtherButtons(parent,buttons, buttons[1]))
        buttons[2].clicked.connect(lambda: disableOtherButtons(parent,buttons, buttons[2]))
        buttons[3].clicked.connect(lambda: disableOtherButtons(parent,buttons, buttons[3]))

        return layout

# make the mc array of buttons single select + update the input field
def disableOtherButtons(parent,buttons, selected):    

    inputField = parent.findChild(QLineEdit,"Input")

    if selected.isChecked():
        
        inputField.setText(selected.objectName())

        for button in buttons:
            if button != selected:
                button.setChecked(False)    
    else:
        inputField.clear()