from PyQt5 import QtCore
from PyQt5.QtWidgets import QCompleter, QLineEdit, QListView
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QCompleter
from utils.autocomplete import process_corpus

import Pages.QAPage.keyboard


class SearchWidget(QLineEdit):
    parent_module = None

    def __init__(self, parent):
        super(SearchWidget, self).__init__(parent)

        self.parent_module = parent

        # create auto completer
        corpus = process_corpus()
        self.completer = QCompleter(corpus, self)
        self.completer.setCompletionMode(QCompleter.InlineCompletion)
        self.setCompleter(self.completer)

        # search widget configurations
        font = QFont()
        font.setPointSize(12)
        self.setFont(font)
        self.setFixedHeight(35)
        self.setAlignment(QtCore.Qt.AlignRight)

        self.textChanged.connect(self._search)

    def _search(self):
        ''' completion is the expected word to be autocompleted for '''

        suggestions = [":)" for i in range(6)]

        # first 3 suggestions are from autocomplete
        i = 0
        while i < 3 and self.completer.setCurrentRow(i):
            suggestions[i] = self.completer.currentCompletion()
            i += 1

        # print(suggestions)

        Pages.QAPage.keyboard.KeyboardInput.changeWordSuggestion(
            self.parent_module, suggestions)
