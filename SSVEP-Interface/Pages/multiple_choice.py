from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton


def multipleChoiceWidget():
    widget = QWidget()
    layout = QGridLayout()
    widget.setLayout(layout)
    labels = [["A", "B"], ["C", "D"]]
    for row in range(len(labels)):
        for col in range(len(labels[0])):
            layout.addWidget(QPushButton(labels[row][col]), row, col)

    return widget
