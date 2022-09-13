from PyQt5.QtWidgets import QLabel,QWidget,QLineEdit, QButtonGroup, QGridLayout, QHBoxLayout, QVBoxLayout
from UI.Components.button_container import ButtonContainer

# groupedChars = ['a | b | c | d | e | f',
#                    'g | h | i | j | k | l',
#                    'm | n | o | p | q | r',
#                    's | t | u | v | w | x',
#                    'y | z | 0 | 1 | 2 | 3',
#                    '4 | 5 | 6 | 7 | 8 | 9']

groupedChars = ['abc | def | ghi',
                'jkl | mno | pqr',
                'stu | vwx | yz0',
                '123 | 456 | 789']

groupedChars2 = [['a | b | c','d | e | f','g | h | i'],
                ['j | k | l','m | n | o','p | q | r'],
                ['s | t | u','v | w | x','y | z | 0'],
                ['1 | 2 | 3','4 | 5 | 6','7 | 8 | 9']]



class KeyboardWidget(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.setObjectName("Keyboard Page")

        layout.addWidget(self.keyboardWidgetUpper(parent))
        layout.addWidget(self.keyboardWidgetLower(parent))

        self.setLayout(layout) 

    def keyboardWidgetUpper(self,parent):
        keyboardKeys = QWidget()
        layout = QHBoxLayout()

        buttons = []
        for x in range(4):
            button = ButtonContainer(groupedChars[x], freqName=f"Keyboard {x+1}", checkable=False)
            buttons.append(button)
            layout.addWidget(button)

        buttons[0].clicked.connect(lambda: keyboardClick(parent,buttons, buttons[0]))
        buttons[1].clicked.connect(lambda: keyboardClick(parent,buttons, buttons[1]))
        buttons[2].clicked.connect(lambda: keyboardClick(parent,buttons, buttons[2]))
        buttons[3].clicked.connect(lambda: keyboardClick(parent,buttons, buttons[3], prediction=True))
        # buttons[4].clicked.connect(lambda: keyboardClick(parent,buttons, buttons[4], prediction=True))
        # buttons[5].clicked.connect(lambda: keyboardClick(parent,buttons, buttons[5], prediction=True))

        keyboardKeys.setLayout(layout)
        return keyboardKeys

    def keyboardWidgetLower(self,parent):
        sidebar = QWidget()
        layout = QHBoxLayout()
        buttons = []

        toggleBtn = ButtonContainer("Toggle Words", freqName="Word Toggle", checkable=False)
        toggleBtn.setObjectName("Toggle")
        buttons.append(toggleBtn)

        buttons.append(ButtonContainer("Space",freqName="Space",checkable=False))
        buttons.append(ButtonContainer("Backspace",freqName="Backspace",checkable=False))

        for button in buttons:
            layout.addWidget(button)

        buttons[0].clicked.connect(lambda:  toggle(parent))
        buttons[1].clicked.connect(lambda: space(parent))
        buttons[2].clicked.connect(lambda: backspace(parent))

        sidebar.setLayout(layout)
        return sidebar

def clickedGroup(parent, buttons, text, level):
    
    if level == 1:
        nextGroup = groupedChars2[groupedChars.index(text)]
        
    elif level == 2:
        nextGroup = list(text.split(' | '))
        print(nextGroup)
    
    for x in range(len(buttons) - 1):
        buttons[x].label.setText(nextGroup[x])

    buttons[3].label.setText("Back")

def clickedBack(parent, buttons, text, level):
    if level == 2:
        for x in range(len(buttons)):
            buttons[x].label.setText(groupedChars[x])

    elif level == 3:
        
        
        currentCharGroup = ""
        for x in range(len(buttons) - 2):
            currentCharGroup +=  buttons[x].label.text()
            currentCharGroup +=  " | "
        currentCharGroup +=  buttons[2].label.text()
        print(currentCharGroup)

        for group in groupedChars2:
            if currentCharGroup in group:
                for x in range(len(buttons)-1):
                    buttons[x].label.setText(groupedChars2[groupedChars2.index(group)][x])
                break



def keyboardClick(parent,buttons,selected,prediction=False):

    toggleBtn = parent.findChild(ButtonContainer,"Toggle")

    btnText = selected.label.text()
    
    if btnText in groupedChars:
        clickedGroup(parent, buttons, btnText, 1)
    elif any(btnText in subl for subl in groupedChars2):
        clickedGroup(parent, buttons, btnText, 2)
    elif btnText == "Back":
        if any(buttons[0].label.text() in subl for subl in groupedChars2):
            clickedBack(parent, buttons, btnText, 2)
        else:
            clickedBack(parent, buttons, btnText, 3)

    elif prediction == True: # Different button functionality when using GTP3 for prediction
        writePredictionToInput(parent, buttons, btnText, charMode=toggleBtn.label.text() == "Toggle Words")
    else:
        writeToInput(parent, buttons, btnText)


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

def backspace(parent):
    inputField = parent.findChild(QLineEdit,"Input")

    temp = inputField.text()

    if len(temp) != 0 :
        inputField.setText(temp[:-1])
        
        #TODO: fix server comm integration
        #parent.parent.emit_message('client_message', {'message': temp[:-1]})

def space(parent):
    inputField = parent.findChild(QLineEdit,"Input")

    temp = inputField.text() + " "
    inputField.setText(temp)
    
    #TODO: fix server comm integration
    #parent.parent.emit_message('client_message', {'message': temp})

def toggle(parent):
    toggleBtn = parent.findChild(ButtonContainer,"Toggle")
    
    if toggleBtn.label.text() == "Toggle Words":
        toggleBtn.label.setText("Toggle Characters")
        # suggestWords(parent)
    else:
        toggleBtn.label.setText("Toggle Words")
        keyboardWidget = parent.findChild(QWidget,"Keyboard Widget")
        keyboardBtns = keyboardWidget.findChildren(ButtonContainer)
        
        for x in range(len(keyboardBtns)):
            keyboardBtns[x].label.setText(groupedChars[x])