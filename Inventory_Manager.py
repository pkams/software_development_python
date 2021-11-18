from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from PyQt5.uic import loadUiType
import sys
from os import path
import sqlite3


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller"""
    base_path = getattr(sys, '_MEIPASS', path.dirname(path.abspath(__file__)))
    return path.join(base_path, relative_path)

FORM_CLASS, _ = loadUiType(resource_path('app_design.ui'))

class Main(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_Buttons()
        self.NAVIGATE()

    def Handel_Buttons(self):
        self.refresh_btn.clicked.connect(self.GET_DATA)
        self.search_btn.clicked.connect(self.SEARCH)
        self.check_btn.clicked.connect(self.LEVEL)
        self.update_btn.clicked.connect(self.UPDATE)
        self.delete_btn.clicked.connect(self.DELETE)
        self.add_btn.clicked.connect(self.ADD)

    def GET_DATA(self):
        db = sqlite3.connect(resource_path('pythonsqlite.db'))
        cursor = db.cursor()
        command = '''SELECT * FROM parts_table'''
        result = cursor.execute(command)

        self.table.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        print('GET_DATA function')

        # Generating statistics
        cursor2 = db.cursor()
        cursor3 = db.cursor()
        cursor4 = db.cursor()
        cursor5 = db.cursor()

        parts_nbr = '''SELECT COUNT (DISTINCT PartName) FROM parts_table'''
        ref_nbr = '''SELECT COUNT (DISTINCT Reference) FROM parts_table'''
        result_ref_nbr = cursor2.execute(parts_nbr)
        result_part_nbr = cursor3.execute(parts_nbr)

        self.lbl_ref_nbr.setText(str(result_ref_nbr.fetchone()[0]))
        self.lbl_part_nbr.setText(str(result_part_nbr.fetchone()[0]))

        # Print results of min, max, etc
        min_hole = '''SELECT MIN(NumberOfHoles), Reference from parts_table'''
        max_hole = '''SELECT MAX(NumberOfHoles), Reference from parts_table'''

        results_min_hole = cursor4.execute(min_hole)
        results_max_hole = cursor5.execute(max_hole)

        r1 = results_min_hole.fetchone()
        r2 = results_max_hole.fetchone()

        # Print results
        self.lbl_min_hole.setText(str(r1[0]))
        self.lbl_max_hole.setText(str(r2[0]))
        self.lbl_min_hole_2.setText(str(r1[1]))
        self.lbl_min_hole_2.setText(str(r2[1]))


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

    def LEVEL(self):
        db = sqlite3.connect('pythonsqlite.db')
        cursor = db.cursor()
        command = '''SELECT Reference, PartName, Count FROM parts_table order by Count asc LIMIT 3'''
        result = cursor.execute(command)

        self.table2.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.table2.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table2.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        print('LEVEL function')

    def NAVIGATE(self):
        db = sqlite3.connect('pythonsqlite.db')
        cursor = db.cursor()
        command = '''SELECT * FROM parts_table'''
        result = cursor.execute(command)

        val = result.fetchone()

        self.id.setText(str(val[0]))
        self.reference.setText(str(val[1]))
        self.partname.setText(str(val[2]))
        self.minarea.setText(str(val[3]))
        self.maxarea.setText(str(val[4]))
        self.nbrofholes.setText(str(val[5]))
        self.mindiameter.setText(str(val[6]))
        self.maxdiameter.setText(str(val[7]))
        self.count.setValue(val[8]) # different method because is a spinbox

    def UPDATE(self):
        db = sqlite3.connect('pythonsqlite.db')
        cursor = db.cursor()

        id_ = int(self.id.text())
        reference_ = self.reference.text()
        partname_ = self.partname.text()
        minarea_ = self.minarea.text()
        maxarea_ = self.maxarea.text()
        nbrofholes_ = self.nbrofholes.text()
        mindiameter_ = self.mindiameter.text()
        maxdiameter_ = self.maxdiameter.text()
        count_ = str(self.count.value())

        row = (reference_, partname_, minarea_, maxarea_, nbrofholes_,
               mindiameter_, maxdiameter_, count_, id_)

        command = """UPDATE parts_table SET Reference = ?,
                                        PartName = ?,
                                        MinArea = ?,
                                        MaxArea = ?,
                                        NumberOfHoles = ?,
                                        MinDiameter = ?,
                                        MaxDiameter = ?,
                                        Count = ? 
                                        WHERE ID = ?"""
        cursor.execute(command, row)

        db.commit()

        print('UPDATE function')

    def DELETE(self):
        db = sqlite3.connect('pythonsqlite.db')
        cursor = db.cursor()
        id_ = self.id.text()

        command = """DELETE FROM parts_table WHERE ID = ?"""
        cursor.execute(command, id_)
        db.commit()

        print('DELETE function')

    def ADD(self):
        db = sqlite3.connect('pythonsqlite.db')
        cursor = db.cursor()

        reference_ = self.reference.text()
        partname_ = self.partname.text()
        minarea_ = self.minarea.text()
        maxarea_ = self.maxarea.text()
        nbrofholes_ = self.nbrofholes.text()
        mindiameter_ = self.mindiameter.text()
        maxdiameter_ = self.maxdiameter.text()
        count_ = str(self.count.value())

        row = (reference_, partname_, minarea_, maxarea_, nbrofholes_,
               mindiameter_, maxdiameter_, count_)

        command = """INSERT INTO parts_table (Reference, PartName, MinArea,
        MaxArea, NumberOfHoles, MinDiameter, MaxDiameter, Count) VALUES (?,?,?,?,?,?,?,?)"""
        cursor.execute(command, row)

        db.commit()

        print('ADD function')

def main():
    app = QApplication(sys.argv)
    window=Main()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()