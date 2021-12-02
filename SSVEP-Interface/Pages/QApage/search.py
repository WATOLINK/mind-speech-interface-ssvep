from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCompleter, QTextEdit
from PyQt5.QtGui import QTextCursor, QKeySequence, QFont

from Pages.QAPage.completer import AutoCompleter

import string


class SearchWidget(QTextEdit):
    def __init__(self, parent=None):
        super(SearchWidget, self).__init__(parent)

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

    def _search(self, completion):
        ''' completion is the expected word to be autocompleted for '''
        tc = self.textCursor()  # get text cursor object (position/other info)

        # find the remaining characters that the user has not typed out yet
        # (full completed word) - (current word in search box) = (trailing charaters)
        trailing = (len(completion) - len(self.completer.completionPrefix()))

        tc.setKeepPositionOnInsert(False)
        tc.movePosition(QTextCursor.Left)
        tc.movePosition(QTextCursor.EndOfWord)

        # add extra space for user to immediately start typing new word
        subText = completion[-trailing:] + " "
        tc.insertText(subText)  # autocomplete

        # perform cursor changes
        self.setTextCursor(tc)

    def focusInEvent(self, event):
        if self.completer:
            self.completer.setWidget(self)
        QTextEdit.focusInEvent(self, event)

    def keyPressEvent(self, event):

        # prevent copy paste
        if event in (QtGui.QKeySequence.Copy, QtGui.QKeySequence.Paste):
            return

        tc = self.textCursor()
        if event.key() == Qt.Key_Tab:
            if self.completer.getSuggestion().strip() != "":
                # on tab we remove our suggestion and autocomplete instead since the user pressed tab
                tc.removeSelectedText()
                self.completer.insertText.emit(self.completer.getSuggestion())
                self.completer.setCompletionMode(QCompleter.InlineCompletion)
                self.completer.reset()
                return

            self.completer.reset()
            tc.setKeepPositionOnInsert(False)
            tc.movePosition(QTextCursor.EndOfWord)
            tc.insertText("\t")
            self.setTextCursor(tc)
            return

        if event.key() == Qt.Key_Space:
            self.completer.reset()
            tc.removeSelectedText()
            tc.setKeepPositionOnInsert(False)
            tc.movePosition(QTextCursor.EndOfWord)
            tc.insertText(" ")
            self.setTextCursor(tc)
            return

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
        self.completer.reset()

        # the key press must be alphanumeric, not a space, and non-empty
        if (event.text().isalnum() or QKeySequence(event.key()).toString() in string.punctuation) and \
                len(tc.selectedText()) > 0:

            # obtain suggestions for current selected text (user's current typed word)
            self.completer.setCompletionPrefix(tc.selectedText())
            self.completer.completionModel().index(0, 0)
            self.completer.complete()

            if self.completer.getSuggestion().strip() == "":
                self.completer.reset()

            # if the autocompleted suggested word is the same as the already typed word
            # (e.g. user typed 'apple' and completer suggests 'apple')
            # we reset the completer's suggestion and just leave the user's word as is
            if self.completer.getSuggestion() == tc.selectedText():
                tc.setKeepPositionOnInsert(False)
                tc.movePosition(QTextCursor.Left)
                tc.movePosition(QTextCursor.EndOfWord)
                # need to reinsert text
                tc.insertText(tc.selectedText())
                self.completer.reset()
            else:
                trailing = (len(self.completer.getSuggestion()) -
                            len(tc.selectedText()))
                tc.setKeepPositionOnInsert(True)
                tc.movePosition(QTextCursor.Left)
                tc.movePosition(QTextCursor.EndOfWord)
                tc.insertText(self.completer.getSuggestion()[-trailing:])

            self.setTextCursor(tc)
