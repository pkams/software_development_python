from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
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
        self.refresh_btn.clicked.connect(self.GET_DATA)
        self.search_btn.clicked.connect(self.SEARCH)

    def GET_DATA(self):
        db = sqlite3.connect('pythonsqlite.db')
        cursor = db.cursor()
        command = '''SELECT * FROM parts_table'''
        result = cursor.execute(command)

        self.table.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        print('GET_DATA function')

        # Generating statistics into the table 2


    def SEARCH(self):
        db = sqlite3.connect('pythonsqlite.db')
        cursor = db.cursor()
        nbr = int(self.count_filter_txt.text())
        command = '''SELECT * FROM parts_table WHERE Count >= {}'''.format(nbr)
        print(command)
        result = cursor.execute(command)

        print(result)
        self.table.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        print('SEARCH function')

    # Here is our code

def main():
    app = QApplication(sys.argv)
    window=Main()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()