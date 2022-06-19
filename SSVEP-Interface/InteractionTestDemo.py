import sys

from PyQt5.QtWidgets import QApplication,QVBoxLayout,QWidget,QHBoxLayout,QSizePolicy,QLineEdit,QLabel
from PyQt5.QtWidgets import QMainWindow

from Pages.styles import windowStyle,textBoxStyle
from Pages.button_container import ButtonContainer

from Pages.HomePage.homepage import promptBox

from InteractionTest.yesno import YesNoWidget


class Window(QMainWindow):
    """Main Window."""

    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)


        self.setWindowTitle('Main Window')  # Sets name of window
        # Adds central widget where we are going to do most of our work

        self.setCentralWidget(HomePageWidget(self))

        # Sets location (x, y) and size (width, height) of current window
        self.setGeometry(0, 0, 1600, 900)



class HomePageWidget(QWidget):
    def __init__(self, parent):
        super().__init__()

        layout = QVBoxLayout()
        
        
        layout.addWidget(promptBox("ඞ"))
        layout.addWidget(inputBox(self))
        layout.addWidget(YesNoWidget(self))
        
        bottomLayout = QHBoxLayout()
        bottomLayout.setStretch(0, 1)
        bottomLayout.setStretch(1, 1)
        bottomLayout.setStretch(2, 1)
        
        confirmButton = ButtonContainer("Confirm", horizontal=True, checkable=False, border=False)
        confirmButton.clicked.connect(lambda: confirm(parent))

        self.dummyWidget = QWidget()
        self.dummyWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        bottomLayout.addWidget(self.dummyWidget) # Dummy widget
        bottomLayout.addWidget(confirmButton)
        bottomLayout.addWidget(self.dummyWidget) # Dummy widget

        layout.addLayout(bottomLayout)

        self.setLayout(layout)

def inputBox(parent):
    textbox = QLineEdit()
    textbox.setStyleSheet(textBoxStyle)
    textbox.setObjectName("Input")
    return textbox

def confirm(parent):
    messageBox = parent.findChild(QLabel,"Prompt")
    inputField = parent.findChild(QLineEdit,"Input")
    currWidget = parent.findChild(QWidget, "YN Widget")

    if inputField.text():
        temp = messageBox.text() + f"[{inputField.text()}]"
        messageBox.setText(temp)
        inputField.clear()

    for button in currWidget.findChildren(ButtonContainer):
        if button.isChecked():
            button.setChecked(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    win = Window()
    win.setStyleSheet(windowStyle)
    win.show()
    sys.exit(app.exec_())
