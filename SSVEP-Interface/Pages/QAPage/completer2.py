from numpy import promote_types
from Pages.button_container import ButtonContainer
from PyQt5.QtWidgets import QWidget, QLineEdit, QCompleter
# from PyQt5.QtGui import QTextCursor, QKeySequence, QFont
from PyQt5 import QtCore
from OpenAI.prediction import OpenAI
import re

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
        self.openAi = OpenAI()

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

    suggestions = ["*"] * 3
    i = 0
    while i < 3 and completer.setCurrentRow(i):
        suggestions[i] = completer.currentCompletion()
        i += 1
    print(suggestions)
    return suggestions

def getPredictions(prompt):
    completer = AutoCompleter()
    prompt = re.sub(' +', ' ', prompt)
    prompt = prompt.rstrip()
    print("P = " + prompt)
    res = completer.openAi.predictWords(prompt=prompt, num_results=20)
    predictions = ["*"] * 3
    i = 0
    while i < 3 and i < len(res):
        predictions[i] = res[i].strip()
        i += 1
    print(predictions)
    return predictions

def suggestWords(parent):

    toggleBtn = parent.findChild(ButtonContainer,"Toggle")

    # means the keyboard is currently on word mode
    if toggleBtn.label.text() == "Toggle Characters":
        
        currentText = parent.findChild(QLineEdit,"Input").text()

        # hard coded prompt for now
        question = "Question: What did you have for dinner last night? Answer: "
        prompt = question + currentText

        lastWord = ""
        print("last:"+currentText+"end")
        if currentText: 
            lastWord = currentText.split()[-1]
        suggestions = getSuggestions(lastWord)

        predictions = ["*"] * 3
        if not currentText or currentText.endswith(' '):
            print("predicted")
            predictions = getPredictions(prompt)

        suggestions = suggestions + predictions

        keyboardWidget = parent.findChild(QWidget,"Keyboard Widget")
        keyboardBtns = keyboardWidget.findChildren(ButtonContainer)

        print("Current Text: "+currentText+"end")
        print("in word mode, making some suggestions")

        # if keyboardBtns[0].label.text() in dummyText:
        for x in range(len(keyboardBtns)):
            keyboardBtns[x].label.setText(suggestions[x])




