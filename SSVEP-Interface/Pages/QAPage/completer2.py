from Pages.button_container import ButtonContainer
from PyQt5.QtWidgets import QWidget, QLineEdit, QCompleter
# from PyQt5.QtGui import QTextCursor, QKeySequence, QFont
from PyQt5 import QtCore

from utils.autocomplete import process_corpus


class Singleton(type(QtCore.QObject), type):
    def __init__(cls, name, bases, dict):
        super().__init__(name, bases, dict)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class AutoCompleter(QCompleter, metaclass=Singleton):
    insertText = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        corpus = process_corpus()

        QCompleter.__init__(self, corpus, parent)
        self.setCompletionMode(QCompleter.InlineCompletion)
        self.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.setMaxVisibleItems(1)
        self.highlighted.connect(self.setHighlighted)
        self.suggestion = ""

    def setHighlighted(self, text):
        self.suggestion = text

    def getSuggestion(self):
        return self.suggestion

    def reset(self):
        self.suggestion = ""

def getSuggestions(text):
    completer = AutoCompleter()
    completer.setCompletionPrefix(text)
    completer.completionModel().index(0, 0)
    completer.complete()

    suggestions = ["*"] * 6
    i = 0
    while i < 3 and completer.setCurrentRow(i):
        suggestions[i] = completer.currentCompletion()
        i += 1
    print(suggestions)
    return suggestions



def suggestWords(parent):

    toggleBtn = parent.findChild(ButtonContainer,"Toggle")

    # means the keyboard is currently on word mode
    if toggleBtn.label.text() == "Toggle Characters":
        
        currentText =   parent.findChild(QLineEdit,"Input").text()
        lastWord = ""
        if currentText: 
            lastWord = currentText.split()[-1]
        suggestions = getSuggestions(lastWord)

        keyboardWidget = parent.findChild(QWidget,"Keyboard Widget")
        keyboardBtns = keyboardWidget.findChildren(ButtonContainer)

        print("Current Text: "+currentText)
        print("in word mode, making some suggestions")

        # if keyboardBtns[0].label.text() in dummyText:
        for x in range(len(keyboardBtns)):
            keyboardBtns[x].label.setText(suggestions[x])




