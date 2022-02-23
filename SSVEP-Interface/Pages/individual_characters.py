from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton

def individualCharacters1Widget(mainStack):
    widget = QWidget()
    layout = QGridLayout()
    labels = [["A", "B", "C"], ["D", "E", "F"]]
    for row in range(len(labels)):
        for col in range(len(labels[0])):
            button = QPushButton(labels[row][col])
            button.clicked.connect(lambda: mainStack.setCurrentIndex(3))
            layout.addWidget(button, row, col)
    widget.setLayout(layout)
    return widget


def individualCharacters2Widget(mainStack):
    widget = QWidget()
    layout = QGridLayout()
    labels = [["G", "H", "I"], ["J", "K", "L"]]
    for row in range(len(labels)):
        for col in range(len(labels[0])):
            button = QPushButton(labels[row][col])
            button.clicked.connect(lambda: mainStack.setCurrentIndex(3))
            layout.addWidget(button, row, col)
    widget.setLayout(layout)
    return widget


def individualCharacters3Widget(mainStack):
    widget = QWidget()
    layout = QGridLayout()
    labels = [["M", "N", "O"], ["P", "Q", "R"]]
    for row in range(len(labels)):
        for col in range(len(labels[0])):
            button = QPushButton(labels[row][col])
            button.clicked.connect(lambda: mainStack.setCurrentIndex(3))
            layout.addWidget(button, row, col)
    widget.setLayout(layout)
    return widget


def individualCharacters4Widget(mainStack):
    widget = QWidget()
    layout = QGridLayout()
    labels = [["S", "T", "U"], ["V", "W", "X"]]
    for row in range(len(labels)):
        for col in range(len(labels[0])):
            button = QPushButton(labels[row][col])
            button.clicked.connect(lambda: mainStack.setCurrentIndex(3))
            layout.addWidget(button, row, col)
    widget.setLayout(layout)
    return widget


def individualCharacters5Widget(mainStack):
    widget = QWidget()
    layout = QGridLayout()
    labels = [["Y", "Z", "0"], ["1", "2", "3"]]
    for row in range(len(labels)):
        for col in range(len(labels[0])):
            button = QPushButton(labels[row][col])
            button.clicked.connect(lambda: mainStack.setCurrentIndex(3))
            layout.addWidget(button, row, col)
    widget.setLayout(layout)
    return widget


def individualCharacters6Widget(mainStack):
    widget = QWidget()
    layout = QGridLayout()
    labels = [["4", "5", "6"], ["7", "8", "9"]]
    for row in range(len(labels)):
        for col in range(len(labels[0])):
            button = QPushButton(labels[row][col])
            button.clicked.connect(lambda: mainStack.setCurrentIndex(3))
            layout.addWidget(button, row, col)
    widget.setLayout(layout)
    return widget