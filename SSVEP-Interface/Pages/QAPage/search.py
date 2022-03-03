import string
import Pages.QAPage.keyboard

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QTextCursor, QKeySequence, QFont

from Pages.QAPage.completer import AutoCompleter


class SearchWidget(QTextEdit):
    parent_module = None

    def __init__(self, parent):
        super(SearchWidget, self).__init__(parent)

        self.parent_module = parent

        # search widget configurations
        font = QFont()
        font.setPointSize(12)
        self.setFont(font)
        self.setFixedHeight(35)
        self.setAlignment(Qt.AlignRight)
        self.setAcceptRichText(False)

        # create auto completer
        self.completer = AutoCompleter()
        self.completer.setWidget(self)

        self.completer.insertText.connect(self._search)

    def _handleTextChange(self):
        '''  text change button update function '''

        suggestions = Pages.QAPage.keyboard.DEFAULT_WORDLIST

        # first 3 suggestions are from autocomplete
        i = 0
        while i < 3 and self.completer.setCurrentRow(i):
            suggestions[i] = self.completer.currentCompletion()
            i += 1

        print(suggestions)

        Pages.QAPage.keyboard.KeyboardInput.changeWordSuggestion(
            self.parent_module, suggestions)

    def _search(self, completion):
        ''' completion is the expected word to be autocompleted for '''
        tc = self.textCursor()  # get text cursor object (position/other info)

        tc.movePosition(QTextCursor.Left)
        tc.movePosition(QTextCursor.EndOfWord)

        tc.insertText(completion)  # autocomplete

        # perform cursor changes
        self.setTextCursor(tc)

    def focusInEvent(self, event):
        if self.completer:
            self.completer.setWidget(self)
        QTextEdit.focusInEvent(self, event)

    def completerReset(self):
        self.completer.reset()

    def useAutoText(self, text):
        self._search(text)

    def keyPressEvent(self, event):
        ''' handle on type event '''

        # prevent copy paste
        if event in (QtGui.QKeySequence.Copy, QtGui.QKeySequence.Paste):
            return

        self._handleTextChange()

        tc = self.textCursor()

        if event.key() == Qt.Key_Backspace:
            self.completer.reset()
            # on backspace we remove the autofill characters
            tc.removeSelectedText()
            # perform backspace command
            tc.deletePreviousChar()
            return

        QTextEdit.keyPressEvent(self, event)
        tc.select(QTextCursor.WordUnderCursor)

        # set completer's suggestion to empty string
        self.completerReset()

        # the key press must be alphanumeric, not a space, and non-empty
        if (event.text().isalnum() or QKeySequence(event.key()).toString() in string.punctuation) and \
                len(tc.selectedText()) > 0:

            # obtain suggestions for current selected text (user's current typed word)
            self.completer.setCompletionPrefix(tc.selectedText())
            self.completer.completionModel().index(0, 0)
            self.completer.complete()

            if self.completer.getSuggestion().strip() == "":
                self.completerReset()

            tc.movePosition(QTextCursor.Left)
            tc.movePosition(QTextCursor.EndOfWord)

        self.setTextCursor(tc)