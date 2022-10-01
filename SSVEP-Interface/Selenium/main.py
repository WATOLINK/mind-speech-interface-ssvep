from operator import index, indexOf
import sre_compile
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap
import sys

import base64, io
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

#prompt = input("Enter the prompt: ")
prompt = "cute dog in suit"

PATH = "C:\Program Files (x86)\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(PATH)

url = "https://www.craiyon.com/"
driver.get(url)

search = driver.find_element(By.ID, "prompt")
search.send_keys(prompt)
search.send_keys(Keys.RETURN)

alt_text = '[alt="' + prompt + '"]'

try:  
    results = WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, alt_text))
    )
    print(results)
except Exception as e:
    print(e)

src = results.get_attribute("src")
# file = open("sample.txt", "r")
# src = file.read()

imgstring = src[len('data:image/jpeg;base64'):]
# imgstring = src

text_file = open("src.txt", "wt")
n = text_file.write(src)

text_file = open("imgstring.txt", "wt")
n = text_file.write(imgstring)

# print(imgstring)

# while (len(imgstring)%4 != 0):
#     imgstring = imgstring[:-1]
# text_file = open("finalstring.txt", "wt")
# n = text_file.write(imgstring)

# Assuming base64_str is the string value without 'data:image/jpeg;base64,'
img = Image.open(io.BytesIO(base64.b64decode(bytes(imgstring, "utf-8"), validate=True)))
img.save('image.png')

# class App(QWidget):

#     def __init__(self):
#         super().__init__()
#         self.title = 'PyQt5 image - pythonspot.com'
#         self.left = 10
#         self.top = 10
#         self.width = 640
#         self.height = 480
#         self.initUI()
    
#     def initUI(self):
#         self.setWindowTitle(self.title)
#         self.setGeometry(self.left, self.top, self.width, self.height)
    
#         # Create widget
#         label = QLabel(self)
#         pixmap = QPixmap()
#         pixmap.loadFromData(baddata)
#         label.setPixmap(pixmap)
#         self.resize(pixmap.width(),pixmap.height())

#         self.show()

# app = QApplication(sys.argv)
# ex = App()

# finalimg = "0xc0" + baddata[indexOf("0xc0"):]



# "b64_data" is a variable containing your base64 encoded jpeg

# label = QLabel(self)
# pixmap = QPixmap('image.png')
# label.setPixmap(pixmap)

# app = QApplication(sys.argv)
# w = QWidget()
# pic = QLabel(w)
# pm = QPixmap()
# pm.loadFromData(finalimg)
# pic.setPixmap(pm)

# w.show()
# app.exec_()