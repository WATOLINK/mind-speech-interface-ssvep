from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QStackedWidget, QVBoxLayout
from Pages.styles import sideBarStyle


def sideBar():
    sidebar = QStackedWidget()

    sidebar = QWidget()
    layout = QGridLayout()
    sidebar.setLayout(layout)
    sidebar.setStyleSheet(sideBarStyle)

    for x in range(4):
        layout.addWidget(QPushButton("poop"), x, 0)
    return sidebar


def characterSideBar():
    sidebar = QWidget()
    layout = QVBoxLayout()
    labels = ["Enter Message", "Backspace", "Space", "Toggle"]
    for row in range(len(labels)):
        layout.addWidget(QPushButton(labels[row]))
    sidebar.setLayout(layout)
    return sidebar


def characterSideBar():
    sidebar = QWidget()
    layout = QVBoxLayout()
    labels = ["Enter Message", "Backspace", "Space", "Toggle"]
    for row in range(len(labels)):
        layout.addWidget(QPushButton(labels[row]))
    sidebar.setLayout(layout)
    return sidebar


def enterOnlySideBar(mainStack):
    # For MC Page and Yes/No Page
    sidebar = QWidget()
    layout = QVBoxLayout()
    button = QPushButton("Enter")
    button.clicked.connect(lambda: mainStack.setCurrentIndex(0))
    layout.addWidget(button)
    sidebar.setLayout(layout)
    return sidebar
