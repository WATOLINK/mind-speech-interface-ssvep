from numpy import promote_types
from UI.Components.button_container import ButtonContainer
from PyQt5.QtWidgets import QWidget, QLineEdit, QCompleter
# from PyQt5.QtGui import QTextCursor, QKeySequence, QFont
from PyQt5 import QtCore
from OpenAI.prediction import OpenAI


from utils.autocomplete import process_corpus
import os
import openai

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

    suggestions = ["*"] * 2
    i = 0
    while i < 2 and completer.setCurrentRow(i):
        suggestions[i] = completer.currentCompletion()
        i += 1
    print(suggestions)
    return suggestions

def getPredictions(prompt):
    completer = AutoCompleter()

    # Clean up prompt for API
    # prompt = re.sub(' +', ' ', prompt)
    # endWithSpace = prompt[len(prompt) - 1] == ' '
    # prompt = prompt.rstrip()

    print("prompt:", prompt)
    openai.api_key = "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"

    res = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=1,
        max_tokens=96,
        top_p=1,
        frequency_penalty=1.14,
        presence_penalty=0
    )
    sentencepredictions = []

    sentencepredictions.append(res)
    print(res)
    pred = res["choices"][0]["text"]
    print(pred)

    sentencepredictions = pred.lstrip("\n").split("\n")
    return sentencepredictions[:3]

    # res = completer.openAi.predictWords(prompt=prompt, num_results=20)
    # predictions = ["*"] * 3
    # i = 0
    # while i < 3 and i < len(res):
    #     if endWithSpace == True:
    #         res[i] = res[i].lstrip()
    #     predictions[i] = res[i]
    #     i += 1
        
    # return predictions

def suggestWords(parent):
    toggleBtn = parent.findChild(ButtonContainer, "Toggle")
    # means the keyboard is currently on word mode
    currentText = parent.findChild(QLineEdit, "Input").text()
    # hard coded prompt for now
    questionInitial = '''
    Answer 3 different and unique ways.
    Question: How are you? Answer: '''
    questionCompletion = '''
    Complete sentence in 3 different and unique ways. “'''
    endSequence = '''__”
    1)
    2)
    3) \n \n '''
    promptInitial = questionInitial + currentText + endSequence
    promptCompletion = questionCompletion + currentText + endSequence
    print(promptCompletion)
    lastWord = ""
    print("last:"+currentText+"end")
    predictions = ["*"] * 3
    suggestions = ["*"] * 3
    if not currentText:
        predictions = getPredictions(promptInitial)
    elif currentText.endswith(' '):
        #predictions = [“test1",“test2”,“test3"]
        predictions = getPredictions(promptCompletion)
    else:
        lastWord = currentText.split()[-1]
        predictions = getPredictions(promptCompletion)
        print(currentText)
        print("Condition 3 is running")
    counter = 0
    for item in predictions:
        if (item[0] == "1" or item[0] == "2" or item[0] == "3"):
            predictions[counter] = item[2:]
        counter = counter + 1
    # for item in predictions:
    #     for char in item:
    #         counter += 1
    #         if char == “,”:
    #             item[counter+1] = ” ”
    print(f"This is the predictions")
    print(predictions)
    suggestions = getSuggestions(lastWord)
    suggestions = suggestions + predictions
    print(suggestions)
    keyboardWidget = parent.findChild(QWidget, "Keyboard Widget")
    keyboardBtns = keyboardWidget.findChildren(ButtonContainer)
    print("Current Text: "+currentText+"end")
    print("in word mode, making some suggestions")
    # if keyboardBtns[0].label.text() in dummyText:
    for x in range(len(keyboardBtns)):
        #Make exception for out of range so that the program doesn't crash
        keyboardBtns[x].label.setText(suggestions[x])
        print(len(keyboardBtns), len(suggestions))

# def suggestWords(parent):

#     toggleBtn = parent.findChild(ButtonContainer,"Toggle")

#     # means the keyboard is currently on word mode
#     if toggleBtn.label.text() == "Toggle Characters":
        
#         currentText = parent.findChild(QLineEdit,"Input").text()

#         # hard coded prompt for now
#         question = "Question: What did you have for dinner last night? Answer: "
#         prompt = question + currentText

#         lastWord = ""
#         print("last:"+currentText+"end")
#         if currentText: 
#             lastWord = currentText.split()[-1]
#         suggestions = getSuggestions(lastWord)

#         predictions = ["*"] * 3
#         if not currentText or currentText.endswith(' '):
#             print("predicted")
#             predictions = getPredictions(prompt)

#         suggestions = suggestions + predictions

#         keyboardWidget = parent.findChild(QWidget,"Keyboard Widget")
#         keyboardBtns = keyboardWidget.findChildren(ButtonContainer)

#         print("Current Text: "+currentText+"end")
#         print("in word mode, making some suggestions")

#         # if keyboardBtns[0].label.text() in dummyText:
#         for x in range(len(keyboardBtns)):
#             keyboardBtns[x].label.setText(suggestions[x])




