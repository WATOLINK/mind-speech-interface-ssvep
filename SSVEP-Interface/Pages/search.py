from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCompleter, QTextEdit
from PyQt5.QtGui import QTextCursor

from Pages.completer import AutoCompleter

NUMERIC = [Qt.Key_1, Qt.Key_2, Qt.Key_3, Qt.Key_4,
           Qt.Key_5, Qt.Key_6, Qt.Key_7, Qt.Key_8, Qt.Key_9]


class SearchWidget(QTextEdit):
    def __init__(self, parent=None):
        super(SearchWidget, self).__init__(parent)

        # search widget configurations
        font = QtGui.QFont()
        font.setPointSize(12)
        self.setFont(font)
        self.setMaximumHeight(30)
        self.setAlignment(Qt.AlignCenter)

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

    # def _cursorInsert(self, cursor, text, keepPos=False):
    #     cursor.setKeepPositionOnInsert(keepPos)
    #     cursor.movePosition(QTextCursor.Left)
    #     cursor.movePosition(QTextCursor.EndOfWord)
    #     cursor.insertText(text)  # autocomplete

    #     # perform cursor changes
    #     self.setTextCursor(cursor)

    def focusInEvent(self, event):
        if self.completer:
            self.completer.setWidget(self)
        QTextEdit.focusInEvent(self, event)

    def keyPressEvent(self, event):

        tc = self.textCursor()
        if event.key() == Qt.Key_Tab:
            # on tab we remove our suggestion and autocomplete instead since the user pressed tab
            tc.removeSelectedText()
            self.completer.insertText.emit(self.completer.getSelected(True))
            self.completer.setCompletionMode(QCompleter.InlineCompletion)
            return

        if event.key() == Qt.Key_Backspace:
            self.completer.resetSelected()

            # on backspace we remove the autofill characters
            tc.removeSelectedText()
            # perform backspace command
            tc.deletePreviousChar()
            return

        QTextEdit.keyPressEvent(self, event)
        tc.select(QTextCursor.WordUnderCursor)

        # set completer's suggestion to empty string
        self.completer.resetSelected()

        # the key press must be alphanumeric, not a space, and non-empty
        if (event.text().isalpha() or event.key() in NUMERIC) and \
                event.key() != Qt.Key_Space and \
                len(tc.selectedText()) > 0:

            # obtain suggestions for current selected text (user's current typed word)
            self.completer.setCompletionPrefix(tc.selectedText())
            self.completer.completionModel().index(0, 0)
            self.completer.complete()

            # if the autocompleted suggested word is the same as the already typed word
            # (e.g. user typed 'apple' and completer suggests 'apple')
            # we reset the completer's suggestion and just leave the user's word as is
            if (self.completer.getSelected() == tc.selectedText()):
                tc.setKeepPositionOnInsert(False)
                tc.movePosition(QTextCursor.Left)
                tc.movePosition(QTextCursor.EndOfWord)
                # need to reinsert text
                tc.insertText(tc.selectedText())

                self.setTextCursor(tc)
            else:
                trailing = (len(self.completer.getSelected()) -
                            len(tc.selectedText()))

                tc.setKeepPositionOnInsert(True)
                tc.movePosition(QTextCursor.Left)
                tc.movePosition(QTextCursor.EndOfWord)
                tc.insertText(self.completer.getSelected()[-trailing:])

                self.setTextCursor(tc)

        elif event.key() == Qt.Key_Space:
            tc.setKeepPositionOnInsert(False)
            tc.movePosition(QTextCursor.Left)
            tc.movePosition(QTextCursor.EndOfWord)
            tc.insertText(" ")

            self.setTextCursor(tc)
