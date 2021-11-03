from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUiType
import sys
from os import path
import sqlite3

FORM_CLASS, _ = loadUiType(path.join(path.dirname('__file__'), 'app_design.ui'))

class Main(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_Buttons()

    def Handel_Buttons(self):
        pass

    # Here is our code

def main():
    app = QApplication(sys.argv)
    window=Main()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()