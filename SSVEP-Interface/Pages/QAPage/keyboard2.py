from PyQt5.QtWidgets import QLabel,QWidget,QLineEdit, QButtonGroup, QGridLayout
from Pages.button_container import ButtonContainer

groupedChars = ['a | b | c | d | e | f',
                   'g | h | i | j | k | l',
                   'm | n | o | p | q | r',
                   's | t | u | v | w | x',
                   'y | z | 0 | 1 | 2 | 3',
                   '4 | 5 | 6 | 7 | 8 | 9']

class KeyboardWidget(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        layout = self.createLayout(parent)
        self.setObjectName("Keyboard Widget")
        self.setLayout(layout)


    def createLayout(self,parent):
        layout = QGridLayout()



        buttons = []
        for x in range(6):
            button = ButtonContainer(groupedChars[x], checkable=False)
            buttons.append(button)
            layout.addWidget(button, int(x/3), x % 3)

        buttons[0].clicked.connect(lambda: keyboardClick(parent,buttons, buttons[0]))
        buttons[1].clicked.connect(lambda: keyboardClick(parent,buttons, buttons[1]))
        buttons[2].clicked.connect(lambda: keyboardClick(parent,buttons, buttons[2]))
        buttons[3].clicked.connect(lambda: keyboardClick(parent,buttons, buttons[3], prediction=True))
        buttons[4].clicked.connect(lambda: keyboardClick(parent,buttons, buttons[4], prediction=True))
        buttons[5].clicked.connect(lambda: keyboardClick(parent,buttons, buttons[5], prediction=True))


        return layout
        


def writeToInput(parent, buttons, text):
    inputField = parent.findChild(QLineEdit,"Input")

    prevText = inputField.text()
    if len(text) == 1:
        for x in range(len(buttons)):
            buttons[x].label.setText(groupedChars[x])
    else:
        prevText =  " ".join(inputField.text().split()[0:-1]) + " "
        text = text + " "
    temp = text
    if prevText:
        temp = prevText + text

    #TODO: fix server comm integration
    # parent.parent.emit_message('client_message', {'message': temp})
    
    inputField.setText(temp)

def writePredictionToInput(parent, buttons, text, charMode):
    inputField = parent.findChild(QLineEdit,"Input")
    prevText = inputField.text()

    # Deletes space between any words and puncuations
    if not text[0].isalpha():
        print("NOT:" + text + "END")
        prevText = prevText.rstrip()

    temp = prevText + text
    
    # If user is typing individual characters
    if charMode == True and len(text) == 1:
        for x in range(len(buttons)):
            buttons[x].label.setText(groupedChars[x])
    else:
        temp += ' '

    inputField.setText(temp)

def clickedGroup(parent, buttons, text):
    charList = list(text.split(' | '))
    print(charList)
    for x in range(len(buttons)):
        buttons[x].label.setText(charList[x])

def keyboardClick(parent,buttons,selected,prediction=False):

    toggleBtn = parent.findChild(ButtonContainer,"Toggle")

    btnText = selected.label.text()
    
    if btnText in groupedChars:
        clickedGroup(parent, buttons, btnText)
    elif prediction == True: # Different button functionality when using GTP3 for prediction
        writePredictionToInput(parent, buttons, btnText, charMode=toggleBtn.label.text() == "Toggle Words")
    else:
        writeToInput(parent, buttons, btnText)
        

