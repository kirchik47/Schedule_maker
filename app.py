# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'menu.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import json
import os
from subprocess import call
import pandas
from pathlib import Path


project_dir = Path(__file__).parent.resolve()
class ShowTable(QtWidgets.QMainWindow):
    # full_sch_class = {}
    def __init__(self, full_sch_class):
        super(ShowTable, self).__init__()
        self.w = None
        self.full_sch_class = full_sch_class
        self.setObjectName("MainWindow")
        # self.setGeometry(200, 100, 600, 400)
        self.showMaximized()
        self.setStyleSheet("background-color: rgb(0, 0, 0)")
        self.centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label = set_widget(self.label, "color: rgb(255, 255, 255)", 'Segoe Print', 48)
        self.label.setGeometry(QtCore.QRect(680, 0, 591, 91))

        self.button_save = QtWidgets.QPushButton("Save schedule", self.centralWidget)
        self.button_save.setGeometry(QtCore.QRect(250, 0, 300, 95))
        self.button_save.setStyleSheet("color: rgb(255, 255, 255);""background-color: rgb(56, 56, 56);\
                                                padding: 20px; margin-right: 10px")
        self.button_save.setFont(QtGui.QFont('Segoe Print', 18))
        self.button_save.clicked.connect(self.save)

        self.button_menu = QtWidgets.QPushButton("Main menu", self.centralWidget)
        self.button_menu.setStyleSheet("color: rgb(255, 255, 255);""background-color: rgb(56, 56, 56);\
                                                padding: 20px; margin-right: 10px")
        self.button_menu.setFont(QtGui.QFont('Segoe Print', 18))
    
        # self.button_menu.setGeometry(QtCore.QRect(0, 0, 100, 30))
        # print(self.button_menu.geometry())
        self.button_menu.clicked.connect(self.show_menu)

        self.table = QtWidgets.QTableWidget(self.centralWidget)
        self.table.setColumnCount(5)

        self.table.setHorizontalHeaderLabels(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
        self.headers = []
        for instance in self.full_sch_class.values():
            self.headers.append(instance.cls)
        self.table.setRowCount(len(self.headers))
        self.table.setVerticalHeaderLabels(self.headers)

        for i in range(len(self.headers)):
            self.table.setRowHeight(i, 300)
        for i in range(5):
            self.table.setColumnWidth(i, 371)
        for i in range(len(self.headers)):
            for j in range(5):
                self.set_widget_cell(i, j)

        self.table.setGeometry(QtCore.QRect(0, 100, 1920, 900))
        self.table.setStyleSheet("background-color: rgb(255, 255, 255)")
        
        # self.button_export = QtWidgets.QPushButton("Export to excel", self.centralWidget)
        # self.button_export = set_widget(self.button_export, 18,
        #                                 "color: rgb(255, 255, 255);""background-color: rgb(56, 56, 56);
        #                                 padding: 50px; margin-top: 50px",
        #                                 'Segoe Print')
        # self.button_export.setGeometry(100, 0, 400, 90)
        # self.button_export.clicked.connect(self.exporter)
        # self.button_export.setAlignment(Qt.AlignTop())
        self.retranslate_ui()

    def save(self):
        data = pandas.DataFrame(index=self.headers, columns=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
        print(data.index)
        for cls in data.index:
            for day in data.columns:
                sch = pandas.Series(index=["1.", "2.", "3.", "4.", "5.", "6.", "7.", "8."])
                for i in range(1, 9):
                    sch[str(i)+"."] = self.full_sch_class[cls].schedule[day][i][0]
                # sch = sch.to_frame()
                # sch = sch.style.set_properties(**{'text-align': 'left'})
                data[day][cls] = str(sch).replace(str('dtype: object'), '')
                print(sch)
        # data_styled = data.style.set_properties(**{'text-align': 'left'})
        # data_styled.set_table_styles([dict(selector='th', props=[('text-align', 'left')])])
        # data_styled = data_styled.to_html()
        # print(data_styled)
        file_name = QtWidgets.QFileDialog.getSaveFileName(self, 
            "Save File", "", "All Files(*);;Text Files(*.txt)")
        file_name = file_name[0]
        if file_name:
            data.to_excel(file_name)
            self.button_save.hide()
            self.save_label = QtWidgets.QLabel(self.centralWidget)
            self.save_label.setText("Saved!")
            # self.save_label.setAlignment(QtCore.Qt.AlignCenter)  # Set alignment to center the text
            self.save_label.setStyleSheet("color: rgb(255, 255, 255)")
            self.save_label.setFont(QtGui.QFont('Segoe Print', 18))
            self.save_label.setGeometry(QtCore.QRect(270, 0, 591, 91))
            self.save_label.show()
            # self.table.hide()
            self.showMaximized()

    def show_menu(self):
        if self.w is None:
            self.w = UiMainWindow()
        self.close()
        self.w.show()

    def set_widget_cell(self, class_index, day_index):
        cls = list(self.full_sch_class.keys())[class_index]
        day = list(self.full_sch_class[cls].schedule.keys())[day_index]
        self.labels = []
        self.widget = QtWidgets.QWidget()
        self.layout = QtWidgets.QVBoxLayout(self.widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        for i in range(1, 9):
            self.table_label = QtWidgets.QLabel(self.widget)
            self.table_label = set_widget(self.table_label, "color: rgb(255, 255, 255)", 'Segoe Print', 9)

            self.table_label.setText(str(i) + '. ' + self.full_sch_class[cls].schedule[day][i][0])

            self.labels.append(self.table_label)

        for label in self.labels:
            self.layout.addWidget(label)
        self.widget.setLayout(self.layout)
        self.table.setCellWidget(class_index, day_index, self.widget)

    # def exporter(self, file_name=None):
    #     if not file_name:
    #         file_name = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', " "'.xlsx', '(*.xlsx)')
    #     if file_name:
    #         print(file_name)
    #         wb = xlsxwriter.Workbook(file_name)
    #         self.sheetBook = wb.add_worksheet()
    #         self.export()
    #         wb.close()
    #
    # def export(self):
    #     row = 0
    #     col = 0
    #     print(self.sheetBook)
    #     print(self.table.rowCount())
    #     for i in range(self.table.columnCount()):
    #         for j in range(self.table.rowCount()):
    #             print(self.table.item(row, col).())
    #             text = str(self.table.item(row, col).text())
    #
    #             self.sheetBook.write(row, col, text)
    #             row += 1
    #             # print("bruh")
    #             # row += 1
    #         row = 0
    #         col += 1

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Schedule Table"))
        # self.save_label.setText(_translate("MainWindow", "Saved!"))


class CreateWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.w = None
        self.resize(1128, 862)
        self.setStyleSheet("background-color: rgb(0, 0, 0)")
        self._translate = QtCore.QCoreApplication.translate
        # self.central_widget = QtWidgets.QWidget()

        # self.setWindowTitle(self._translate("main_window", "main_window"))

        # self.label_2.setText(_translate("main_window", "Enter teachers info:"))

        self.vertical_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.vertical_widget)
        # self.vertical_widget.setGeometry(QtCore.QRect(20, 140, 320, 421))

        # self.horizontal_widget = QtWidgets.QWidget(self.vertical_widget)
        # self.horizontal_widget.setGeometry(QtCore.QRect(0, 40, 600, 100))
        #
        # self.horizontal_layout = QtWidgets.QVBoxLayout(self.horizontal_widget)
        # self.horizontal_layout.setContentsMargins(0, 0, 0, 0)

        self.vertical_layout = QtWidgets.QVBoxLayout()
        self.vertical_layout.setAlignment(Qt.AlignTop)
        self.vertical_layout.setContentsMargins(0, 0, 0, 0)

        self.button_menu = QtWidgets.QPushButton("Main menu", self.vertical_widget)
        self.button_menu = set_widget(self.button_menu,
                                      "color: rgb(255, 255, 255);""background-color: rgb(56, 56, 56);\
                                                padding: 20px; margin-right: 1000px",
                                      'Segoe Print', 18)
        self.button_menu.clicked.connect(self.show_menu)
        # self.button_menu.setGeometry(100, 0, 400, 90)
        self.vertical_layout.addWidget(self.button_menu)

        self.label = QtWidgets.QLabel(self._translate("main_window", "Create schedule"))
        # self.label.setGeometry(QtCore.QRect(240, 20, 661, 121))
        self.label.setAlignment(Qt.AlignCenter)
        self.label = set_widget(self.label,
                                "color: rgb(255, 255, 255)", 'Segoe Print', 48)

        self.vertical_layout.addWidget(self.label)

        self.label_file = QtWidgets.QLabel(self._translate("main_window", "Choose teachers file: "))
        # self.label_file.setAlignment(Qt.AlignCenter)
        self.label_file = set_widget(self.label_file, "color: rgb(255, 255, 255); margin-left: 200px", 'Segoe Print', 24)
        self.vertical_layout.addWidget(self.label_file)

        # self.amount = QtWidgets.QLineEdit(self.horizontal_widget)
        # self.amount = set_widget(self.amount, 18, "color: rgb(255, 255, 255)", 'Segoe Print')
        # self.horizontal_layout.addWidget(self.amount)

        self.button_submit = QtWidgets.QPushButton(self._translate("main_window", "Teachers file"))
        self.button_submit = set_widget(self.button_submit,
                                        "color: rgb(255, 255, 255);""background-color: rgb(56, 56, 56);"
                                        " padding: 50px; margin-left: 200px; margin-right: 200px",
                                        'Segoe Print', 24)
        self.button_submit.clicked.connect(self.get_file)
        self.vertical_layout.addWidget(self.button_submit)


        self.vertical_widget.setLayout(self.vertical_layout)
        self.ind = 0
        # self.retranslate_ui(self)

    def show_menu(self):
        if self.w is None:
            self.w = UiMainWindow()
        self.close()
        self.w.show()

    def get_file(self):
        def add_data():
            with open(os.path.join(project_dir, 'temp_data.txt'), 'a+') as f:
                    temp = f.read()
                    f.write(temp+' '+file_name)
        
        self.file = QtWidgets.QFileDialog(self.vertical_widget)
        file_name = self.file.getOpenFileName()[0]
        if file_name:
            self.ind += 1
            with open(file_name, 'r') as f:
                print(file_name)
                data = json.load(f)
                # print(type(data))
                if self.ind == 1:
                    teachers = data
                    with open(file_name, 'w') as f:
                        json.dump(teachers, f)
                    add_data()
                    self.label_file.setText("Choose subjects file: ")
                    self.button_submit.setText("Subjects file")
                if self.ind == 2:
                    subjects = data
                    with open(file_name, 'w') as f:
                        json.dump(subjects, f)
                    add_data()
                    self.label_file.setText("Choose classes file: ")
                    self.button_submit.setText("Classes file")
                if self.ind == 3:
                    classes = data
                    with open(file_name, 'w') as f:
                        json.dump(classes, f)
                    add_data()
                    self.close()
                    os.system(f"py {os.path.join(project_dir, 'schedule.py')}")
                    self.close()


    # def teachers_list(self):
    #     try:
    #         for ind in range(int(self.amount.text())):
    #             pass
    #     except:
    #         if self.amount.text():
    #             error_label = QtWidgets.QLabel(self.vertical_widget)
    #             error_label.setText("An error occured. Please enter number")
    #             error_label = set_widget(error_label, 18,
    #                                      "color: rgb(255, 255, 255)", 'Segoe Print')
    #             self.vertical_layout.addWidget(error_label)

    # def retranslate_ui(self, main_window):
    #     _translate = QtCore.QCoreApplication.translate
    #     main_window.setWindowTitle(_translate("main_window", "main_window"))
    #     self.label.setText(_translate("main_window", "Create schedule"))
    #     # self.label_2.setText(_translate("main_window", "Enter teachers info:"))
    #     self.label_file.setText(_translate("main_window", "Choose teachers file: "))
    #     self.button_submit.setText(_translate("main_window", "Teachers file"))


class InstructionWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1128, 862)
        self.w = None
        self.setStyleSheet("background-color: rgb(0, 0, 0)")
        # self.central_widget = QtWidgets.QScrollArea()
        # self.central_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # self.central_widget.setFixedHeight(800)
        # self.central_widget.setWidgetResizable(True)
        # self.central_widget.setGeometry(10, 10, 1161, 1000)
        # self.setCentralWidget(self.central_widget)

        self.widget = QtWidgets.QWidget()

        self.vertical_layout = QtWidgets.QVBoxLayout()
        self.button_menu = QtWidgets.QPushButton("Main menu", self.widget)
        self.button_menu = set_widget(self.button_menu,
                                      "color: rgb(255, 255, 255);""background-color: rgb(56, 56, 56);\
                                                        padding: 20px; margin-right: 1000px",
                                      'Segoe Print', 18)
        self.button_menu.clicked.connect(self.show_menu)
        self.vertical_layout.addWidget(self.button_menu)
        # self.label.setGeometry(QtCore.QRect(10, 10, 1161, 121))
        # self.vertical_layout.setContentsMargins(0, 100, 0, 100)
        # self.central_widget.setLayout(self.vertical_layout)

        # self.label = QtWidgets.QLabel(self.central_widget)
        # # self.label.setGeometry(QtCore.QRect(10, 10, 1161, 121))
        # self.label = set_widget(self.label,
        #                         "color: rgb(255, 255, 255)", 'Segoe Print')
        # self.vertical_layout.addWidget(self.label)
        content = get_file()
        for text in content:
            label_instruction = QtWidgets.QLabel(text)
            # label_instruction.setContentsMargins(0, 100, 0, 100)

            label_instruction = set_widget(label_instruction,
                                           "color: rgb(255, 255, 255)",
                                           'Segoe Print', 9)
            label_instruction.setStyleSheet("color: rgb(255, 255, 255)")
            # label_instruction.resize(200, 200)
            self.vertical_layout.addWidget(label_instruction, 0)

        self.widget.setLayout(self.vertical_layout)
        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        # self.scroll.setFixedHeight(800)
        # self.vertical_layout.addWidget(self.scroll)

        self.scroll.setWidget(self.widget)

        self.setCentralWidget(self.scroll)
        self.retranslate_ui(self)

    def show_menu(self):
        if self.w is None:
            self.w = UiMainWindow()
        self.close()
        self.w.show()

    def retranslate_ui(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "main_window"))
        # self.label.setText(_translate("main_window", "Instructions to json format"))


class UiMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(UiMainWindow, self).__init__()
        self.w = None
        self.setObjectName("MainWindow")
        self.resize(1128, 862)
        self.setStyleSheet("background-color: rgb(0, 0, 0)")
        self.centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralWidget)

        # self.verticalWidget = QtWidgets.QWidget(self.centralWidget)
        # self.verticalWidget.setGeometry(QtCore.QRect(280, 260, 581, 421))

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setContentsMargins(200, 0, 200, 0)
        # self.verticalLayout.setGeometry(QtCore.QRect(280, 260, 581, 421))
        self.verticalLayout.setAlignment(Qt.AlignTop)
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setAlignment(Qt.AlignCenter)
        self.label = set_widget(self.label, "color: rgb(255, 255, 255)", 'Segoe Print', 48)
        # self.label.setGeometry(QtCore.QRect(280, 0, 591, 91))
        self.verticalLayout.addWidget(self.label)

        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setAlignment(Qt.AlignCenter)
        # self.label_2.setMargin()
        self.label_2 = set_widget(self.label_2,
                                  "color: rgb(255, 255, 255);", 'Segoe Print', 36)
        # self.label_2.setGeometry(QtCore.QRect(400, 120, 351, 61))
        self.verticalLayout.addWidget(self.label_2)

        self.button_create = QtWidgets.QPushButton()
        self.button_create = set_widget(self.button_create,
                                        "color: rgb(255, 255, 255);" "background-color: rgb(56, 56, 56); margin: 20px; "
                                        "padding: 20px",
                                        point_size=24)
        self.button_create.clicked.connect(self.show_create_window)
        self.verticalLayout.addWidget(self.button_create)

        self.button_saved = QtWidgets.QPushButton()
        self.button_saved = set_widget(self.button_saved,
                                       "color: rgb(255, 255, 255);" "background-color: rgb(56, 56, 56); margin: 20px; "
                                       "padding: 20px",
                                       point_size=24)

        self.verticalLayout.addWidget(self.button_saved)

        self.button_instruction = QtWidgets.QPushButton()
        self.button_instruction = set_widget(self.button_instruction,
                                             "color: rgb(255, 255, 255);" "background-color: rgb(56, 56, 56); "
                                             "margin: 20px; padding: 20px",
                                             point_size=24)
        self.button_instruction.clicked.connect(self.show_instruction_window)
        self.verticalLayout.addWidget(self.button_instruction)

        self.retranslate_ui()

    def show_create_window(self):
        if self.w is None:

            self.w = CreateWindow()
        self.close()
        self.w.show()

    def show_instruction_window(self):
        if self.w is None:
            self.w = InstructionWindow()

        self.close()
        self.w.show()

    def retranslate_ui(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.button_create.setText(_translate("MainWindow", "CREATE"))
        self.button_saved.setText(_translate("MainWindow", "SAVED SCHEDULES"))
        self.button_instruction.setText(_translate("MainWindow", "JSON INSTRUCTIONS"))
        self.label.setText(_translate("MainWindow", "Schedule App"))
        self.label_2.setText(_translate("MainWindow", "Main menu"))


def get_file(file_name=os.path.join(project_dir, 'instruction.txt'), mode='r'):
    with open(file_name, mode) as f:
        content = f.readlines()
        content = [el.strip() for el in content]
        # print(content)

    return content


def set_widget(widget, style_sheet, family=None, point_size=None, auto_fill=True):
    font = QtGui.QFont()
    if family:
        font.setFamily(family)
    if point_size:
        font.setPointSize(point_size)
    widget.setFont(font)
    widget.setAutoFillBackground(auto_fill)
    widget.setStyleSheet(style_sheet)
    return widget


if __name__ == "__main__":
    with open(os.path.join(project_dir, 'temp_data.txt'), 'w') as f:
        f.write(' ')
    app = QtWidgets.QApplication(sys.argv)
    ui = UiMainWindow()
    ui.show()

    app.exec_()

