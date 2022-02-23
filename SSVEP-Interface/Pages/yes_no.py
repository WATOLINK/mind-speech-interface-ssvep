from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton


def yesNoWidget():
    widget = QWidget()
    layout = QHBoxLayout()
    labels = ["Yes/True", "No/False"]
    for col in range(len(labels)):
        layout.addWidget(QPushButton(labels[col]))
    widget.setLayout(layout)
    return widget
