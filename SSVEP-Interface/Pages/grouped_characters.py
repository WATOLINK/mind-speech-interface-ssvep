from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton


def groupedCharacterWidget(mainStack):
    widget = QWidget()
    layout = QGridLayout()
    labels = ["ABCDEF", "GHIJKL", "MNOPQR", "STUVWX", "YZ0123", "456789"]

    buttonArray = []
    for x in range(6):
        button = QPushButton(labels[x])
        buttonArray.append(button)
        layout.addWidget(button, int(x/3), x % 3)

    # when you do this with a for loop, it dont wory, we don't know why
    # but hardcoding works! so haha!
    buttonArray[0].clicked.connect(lambda: mainStack.setCurrentIndex(4))
    buttonArray[1].clicked.connect(lambda: mainStack.setCurrentIndex(5))
    buttonArray[2].clicked.connect(lambda: mainStack.setCurrentIndex(6))
    buttonArray[3].clicked.connect(lambda: mainStack.setCurrentIndex(7))
    buttonArray[4].clicked.connect(lambda: mainStack.setCurrentIndex(8))
    buttonArray[5].clicked.connect(lambda: mainStack.setCurrentIndex(9))

    widget.setLayout(layout)
    return widget
