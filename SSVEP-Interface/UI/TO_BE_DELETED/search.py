import string
# import UI.KeyboardPage.keyboard
import TEMP_ARCHIVE.keyboard

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QTextCursor, QKeySequence, QFont

from UI.KeyboardPage.completer import AutoCompleter


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

        # do not modify original
        suggestions = UI.KeyboardPage.keyboard.DEFAULT_WORDLIST[:]
        # first 3 suggestions are from autocomplete
        i = 0
        while i < 3 and self.completer.setCurrentRow(i):
            suggestions[i] = self.completer.currentCompletion()
            i += 1

        print(suggestions)

        UI.KeyboardPage.keyboard.KeyboardInput.changeWordSuggestion(
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
        # clear buttons
        UI.KeyboardPage.keyboard.KeyboardInput.changeWordSuggestion(
            self.parent_module, UI.KeyboardPage.keyboard.DEFAULT_WORDLIST)

    def useAutoText(self, text):
        self._search(text)

    def clearDisplay(self, clearAll=False):
        cursor = self.textCursor()
        if clearAll:
            cursor.movePosition(QTextCursor.Left)
            cursor.movePosition(QTextCursor.EndOfWord)
            cursor.select(QTextCursor.WordUnderCursor)
        cursor.deletePreviousChar()

    def keyPressEvent(self, event):
        ''' handle on type event '''
        # prevent copy paste
        if event in (QtGui.QKeySequence.Copy, QtGui.QKeySequence.Paste):
            return
        print("kb event triggered")
        QTextEdit.keyPressEvent(self, event)
        self.updateCompleter(event.text(), event.key())

    def updateCompleter(self, text, key):
        tc = self.textCursor()
        tc.movePosition(QTextCursor.Left)
        tc.movePosition(QTextCursor.EndOfWord)
        tc.select(QTextCursor.WordUnderCursor)
        # set completer's suggestion to empty string
        self.completerReset()

        # the key press must be alphanumeric, not a space, and non-empty
        if (key == Qt.Key_Backspace or text.isalnum() or QKeySequence(key).toString() in string.punctuation) and \
                len(tc.selectedText()) > 0:

            # obtain suggestions for current selected text (user's current typed word)
            self.completer.setCompletionPrefix(tc.selectedText())
            self.completer.completionModel().index(0, 0)
            self.completer.complete()

            self._handleTextChange()

            if self.completer.getSuggestion().strip() == "":
                self.completerReset()

        tc.movePosition(QTextCursor.Left)
        tc.movePosition(QTextCursor.EndOfWord)
        self.setTextCursor(tc)
