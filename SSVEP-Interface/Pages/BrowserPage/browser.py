import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class Browser(QWebEngineView):
    def __init__(self, url):
        print("1")
        super().__init__()
        self.loadProgress.connect(print)
        self.load(QUrl(url))
        self.loadFinished.connect(self.pageReady)
        print("2")

    def pageReady(self, success):
        if success:
            self.resize(1600, 900)
            self.show()
        else:
            print('page failed to load')
        print("3")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    browser = Browser("https://www.craiyon.com/")
    app.exec_()