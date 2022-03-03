from PyQt5.QtWidgets import QCompleter
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
