import sys
from PyQt5 import QtWidgets
import json
from copy import deepcopy
from app import ShowTable
import os

sys.setrecursionlimit(10000)

project_dir = "C:\\Users\\kirch\\pythonProject\\final_project"
class ScheduleClass:
    def __init__(self, cls, hours):
        self.cls = cls
        self.hours = hours
        self.min_lessons = hours // 5
        self.max_lessons_amount = hours % 5
        # setting default schedule with empty cells
        self.schedule = {day: {} for day in ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday')}
        for day_sch in self.schedule.values():
            day_sch.update({index: ['', ''] for index in range(1, 10)})

    def __str__(self):
        return {self.cls: self.hours}


class ScheduleTeacher:
    def __init__(self, name, hours):
        self.name = name
        self.hours = hours
        # setting default schedule with empty cells
        self.schedule = {day: {} for day in ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday')}
        for day_sch in self.schedule.values():
            day_sch.update({index: {} for index in range(1, 9)})


def create_schedule(cur_subject, num, letter, flag_replace=False, prev=[]):
    res = False

    def check_res():
        nonlocal res
        if res is True:
            return res
        if res == "found":
            if list(classes[num].keys())[-1] == letter:
                if num == "11":
                    res = create_schedule(cur_subject, "5", "a", flag_replace)
                else:
                    res = create_schedule(cur_subject, str(int(num) + 1), "a", flag_replace)
            else:
                res = create_schedule(cur_subject, num,
                                      list(classes[num])[list(classes[num]).index(letter) + 1], flag_replace)
        if res:
            return res

    def check_position():
        return i <= schedule_instance_class.min_lessons or (i == schedule_instance_class.min_lessons + 1 and
                                                            schedule_instance_class.max_lessons_amount > 0)

    def check_max_lessons():
        if i == schedule_instance_class.min_lessons + 1:
            schedule_instance_class.max_lessons_amount -= 1

    def add_max_amount():
        if i == schedule_instance_class.min_lessons + 1:
            schedule_instance_class.max_lessons_amount += 1

    def check_banned_subjects():
        for banned_subj in subjects[cur_subject]["banned_subjects"]:
            # print(list(sch.values()))
            if banned_subj in sub_list:
                return True
        return False

    def check_pairs():
        return (not is_paired and cnt == 1) or (is_paired and cnt == 2) or \
               (is_paired and i != 1 and schedule[i - 1][0] != cur_subject and
                schedule[i + 1][0] != cur_subject and cnt == 1)

    def to_the_first_class():
        nonlocal res
        if num == "11" and list(classes[num].keys())[-1] == letter:
            res = create_schedule(cur_subject, "5", "a", flag_replace)
            return res
        return False

    def next_class():
        nonlocal res
        if list(classes[num].keys())[-1] == letter:
            res = create_schedule(cur_subject, str(int(num) + 1), "a", flag_replace)
            return res

    schedule_instance_class = full_sch_class[f"{num}-{letter}"]
    if res is True:
        return res
    if subjects[cur_subject]["hours"] <= 0:
        subjects[cur_subject]["hours"] = 0
        if flag_replace:
            return "found"
        try:
            res = create_schedule(list(subjects.keys())[list(subjects.keys()).index(cur_subject) + 1], "5", "a")
            if res is True:
                return res
        except IndexError:
            return True
    if cur_subject not in list(classes[num][letter].keys()) or classes[num][letter][cur_subject]["hours"] <= 0:
        if cur_subject in list(classes[num][letter].keys()):
            classes[num][letter][cur_subject]["hours"] = 0
        temp_res = to_the_first_class()
        if temp_res:
            return temp_res
        else:
            temp_res = next_class()
            if temp_res:
                res = temp_res
            else:
                res = create_schedule(cur_subject, num, list(classes[num])[list(classes[num]).index(letter) + 1], flag_replace)
            return res
    # else:
    #     if list(classes[num].keys())[-1] == letter and num != "11":
    #         res = create_schedule(cur_subject, str(int(num) + 1), "a", f)
    #     elif num == "11" and list(classes[num].keys())[-1] == letter:
    #         res = create_schedule(cur_subject, "5", "a", f)
    #     else:
    #         res = create_schedule(cur_subject, num, list(classes[num])[list(classes[num]).index(letter) + 1], f)
    #
    #     return res
    # iterating for schedules for this class
    for day, schedule in schedule_instance_class.schedule.items():
        print(schedule)
        for i, data in schedule.items():
            if i == 9:
                continue
            lesson = data[0]

            if not lesson and cur_subject not in prev:

                if check_position():
                    
                    if i > 1 and schedule[i - 1] == cur_subject and not classes[num][letter][cur_subject]["can_be_paired"]:
                        break
                    else:
                        sub_list = [subli[0] for subli in list(schedule.values())]
                        if check_banned_subjects():
                            break
                        is_paired = classes[num][letter][cur_subject]["can_be_paired"]
                        cnt = sub_list.count(cur_subject)
                        if check_pairs():
                            break
                        amount_of_teachers = len(classes[num][letter][cur_subject]["teachers"])
                        check_max_lessons()
                        for teacher_ind in range(amount_of_teachers):
                            # print(num, letter)
                            teacher = classes[num][letter][cur_subject]["teachers"][teacher_ind]
                            schedule_instance_teacher = full_sch_teacher[teacher]
                            if schedule_instance_teacher.schedule[day][i] != {}:
                                continue
                            teachers[teacher] -= 1
                            if teachers[teacher] >= 0:

                                schedule[i] = [cur_subject, teacher]
                                subjects[cur_subject]["hours"] -= 1
                                classes[num][letter][cur_subject]["hours"] -= 1
                                schedule_instance_teacher.schedule[day][i] = {cur_subject: f"{num}-{letter}"}
                                temp_res = to_the_first_class()
                                if temp_res:
                                    return temp_res
                                else:
                                    temp_res = next_class()
                                    if temp_res:
                                        res = temp_res
                                    else:
                                        res = create_schedule(cur_subject, num,
                                                              list(classes[num])[list(classes[num]).index(letter) + 1],
                                                              flag_replace)
                                    if res:
                                        return res

                                schedule[i] = ['', '']
                                schedule_instance_teacher.schedule[day][i] = {}
                                classes[num][letter][cur_subject]["hours"] += 1
                                subjects[cur_subject]["hours"] += 1
                            teachers[teacher] += 1

                        if i == schedule_instance_class.min_lessons + 1:
                            schedule_instance_class.max_lessons_amount += 1

    for day, schedule in schedule_instance_class.schedule.items():
        for i, data in schedule.items():
            if i == 9:
                continue
            lesson = data[0]
            if "/" not in lesson and lesson != cur_subject and lesson not in prev:
                if check_position():
                    check_max_lessons()
                    cur_subject_in_schedule = deepcopy(schedule[i])
                    amount_of_teachers = len(classes[num][letter][cur_subject]["teachers"])
                    sub_list = [subli[0] for subli in list(schedule.values())]
                    is_paired = classes[num][letter][cur_subject]["can_be_paired"]
                    cnt = sub_list.count(cur_subject)
                    if check_pairs():
                        break
                    schedule[i][0] = cur_subject
                    if check_banned_subjects():
                        schedule[i][0] = cur_subject_in_schedule[0]
                        continue

                    for teacher_ind in range(amount_of_teachers):

                        teacher = classes[num][letter][cur_subject]["teachers"][teacher_ind]
                        schedule_instance_teacher = full_sch_teacher[teacher]

                        if schedule_instance_teacher.schedule[day][i] != {} and cur_subject not in prev and lesson == '':

                            temp2 = list(schedule_instance_teacher.schedule[day][i].keys()) + list(
                                schedule_instance_teacher.schedule[day][i].values())
                            # schedule_instance_teacher_temp.schedule[day][i] = {}
                            num_temp = ''
                            for symbol in temp2[1]:
                                if symbol == '-':
                                    break
                                num_temp += symbol
                            letter_temp = ''
                            flag = 0
                            for symbol in temp2[1]:
                                if flag == 1:
                                    letter_temp += symbol
                                if symbol == '-':
                                    flag = 1

                            temp_instance = full_sch_class[f"{num_temp}-{letter_temp}"]
                            sch_temp = temp_instance.schedule[day]
                            sch_temp[i][0] = ''
                            sch_temp[i][1] = ''

                            schedule[i][0] = cur_subject
                            schedule[i][1] = teacher

                            subjects[temp2[0]]["hours"] += 1
                            subjects[cur_subject]["hours"] -= 1

                            classes[num_temp][letter_temp][temp2[0]]["hours"] += 1
                            classes[num][letter][cur_subject]["hours"] -= 1

                            schedule_instance_teacher.schedule[day][i] = {cur_subject: f"{num}-{letter}"}
                            res = create_schedule(temp2[0], num_temp, letter_temp, True, prev + [cur_subject])
                            temp = check_res()
                            if temp:
                                return temp
                            schedule[i][0] = temp2[0]
                            subjects[temp2[0]]["hours"] -= 1
                            subjects[cur_subject]["hours"] += 1

                            classes[num][letter][temp2[0]]["hours"] -= 1
                            schedule_instance_teacher.schedule[day][i] = {'': ''}

                            continue
                        print(cur_subject_in_schedule)
                        schedule_instance_teacher_temp = full_sch_teacher[cur_subject_in_schedule[1]]
                        schedule_instance_teacher_temp.schedule[day][i] = {}

                        schedule[i][0] = cur_subject
                        schedule[i][1] = teacher

                        subjects[cur_subject_in_schedule[0]]["hours"] += 1
                        subjects[cur_subject]["hours"] -= 1

                        classes[num][letter][cur_subject_in_schedule[0]]["hours"] += 1
                        classes[num][letter][cur_subject]["hours"] -= 1

                        teachers[cur_subject_in_schedule[1]] += 1
                        teachers[teacher] -= 1

                        schedule_instance_teacher.schedule[day][i] = {cur_subject: f"{num}-{letter}"}

                        res = create_schedule(cur_subject_in_schedule[0], num, letter, True, prev + [cur_subject])

                        temp = check_res()
                        if temp:
                            return temp
                        schedule[i][0] = cur_subject_in_schedule[0]
                        schedule[i][1] = cur_subject_in_schedule[1]

                        subjects[cur_subject_in_schedule[0]]["hours"] -= 1
                        subjects[cur_subject]["hours"] += 1

                        classes[num][letter][cur_subject]["hours"] += 1
                        classes[num][letter][cur_subject_in_schedule[0]]["hours"] -= 1

                        teachers[cur_subject_in_schedule[1]] -= 1
                        teachers[teacher] += 1

                        schedule_instance_teacher_temp.schedule[day][i] = {cur_subject_in_schedule[0]:
                                                                           cur_subject_in_schedule[1]}
                        schedule_instance_teacher.schedule[day][i] = {'': ''}
                    schedule[i][0] = cur_subject_in_schedule[0]

    return False


# class UiMainWindow(QtWidgets.QMainWindow):
#     def __init__(self, ):
#         super(UiMainWindow, self).__init__()
#         self.w = None
#         self.setObjectName("MainWindow")
#         # self.setGeometry(200, 100, 600, 400)
#         self.showMaximized()
#         self.setStyleSheet("background-color: rgb(0, 0, 0)")
#         self.centralWidget = QtWidgets.QWidget(self)
#
#         self.label = QtWidgets.QLabel(self.centralWidget)
#         self.label = set_widget(self.label, 48,
#                                 "color: rgb(255, 255, 255)", 'Segoe Print')
#         self.label.setGeometry(QtCore.QRect(680, 0, 591, 91))
#
#         self.table = QtWidgets.QTableWidget(self.centralWidget)
#         self.table.setColumnCount(5)
#
#         self.table.setHorizontalHeaderLabels(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
#         self.headers = []
#         for instance in full_sch_class.values():
#             self.headers.append(instance.cls)
#         self.table.setRowCount(len(self.headers))
#         self.table.setVerticalHeaderLabels(self.headers)
#
#         for i in range(len(self.headers)):
#             self.table.setRowHeight(i, 300)
#         for i in range(5):
#             self.table.setColumnWidth(i, 371)
#         for i in range(len(self.headers)):
#             for j in range(5):
#                 self.set_widget_cell(i, j)
#
#         self.table.setGeometry(QtCore.QRect(0, 100, 1920, 900))
#         self.table.setStyleSheet("background-color: rgb(255, 255, 255)")
#         self.setCentralWidget(self.centralWidget)
#         # self.button_export = QtWidgets.QPushButton("Export to excel", self.centralWidget)
#         # self.button_export = set_widget(self.button_export, 18,
#         #                                 "color: rgb(255, 255, 255);""background-color: rgb(56, 56, 56); padding: 50px; margin-top: 50px",
#         #                                 'Segoe Print')
#         # self.button_export.setGeometry(100, 0, 400, 90)
#         # self.button_export.clicked.connect(self.exporter)
#         # self.button_export.setAlignment(Qt.AlignTop())
#         self.retranslate_ui()
#
#     def set_widget_cell(self, class_index, day_index):
#         cls = list(full_sch_class.keys())[class_index]
#         day = list(full_sch_class[cls].schedule.keys())[day_index]
#         self.labels = []
#         self.widget = QtWidgets.QWidget()
#         self.layout = QtWidgets.QVBoxLayout(self.widget)
#         self.layout.setContentsMargins(0, 0, 0, 0)
#         for i in range(1, 9):
#             self.table_label = QtWidgets.QLabel(self.widget)
#             self.table_label = set_widget(self.table_label, 9,
#                                           "color: rgb(255, 255, 255)", 'Segoe Print')
#
#             self.table_label.setText(str(i) + '. ' + full_sch_class[cls].schedule[day][i][0])
#
#             self.labels.append(self.table_label)
#
#         for label in self.labels:
#             self.layout.addWidget(label)
#         self.widget.setLayout(self.layout)
#         self.table.setCellWidget(class_index, day_index, self.widget)
#
#     # def exporter(self, file_name=None):
#     #     if not file_name:
#     #         file_name = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', " "'.xlsx', '(*.xlsx)')
#     #     if file_name:
#     #         print(file_name)
#     #         wb = xlsxwriter.Workbook(file_name)
#     #         self.sheetBook = wb.add_worksheet()
#     #         self.export()
#     #         wb.close()
#     #
#     # def export(self):
#     #     row = 0
#     #     col = 0
#     #     print(self.sheetBook)
#     #     print(self.table.rowCount())
#     #     for i in range(self.table.columnCount()):
#     #         for j in range(self.table.rowCount()):
#     #             print(self.table.item(row, col).())
#     #             text = str(self.table.item(row, col).text())
#     #
#     #             self.sheetBook.write(row, col, text)
#     #             row += 1
#     #             # print("bruh")
#     #             # row += 1
#     #         row = 0
#     #         col += 1
#
#     def retranslate_ui(self):
#         _translate = QtCore.QCoreApplication.translate
#         self.setWindowTitle(_translate("MainWindow", "MainWindow"))
#         self.label.setText(_translate("MainWindow", "Schedule Table"))


# def set_widget(widget, point_size, style_sheet, family='', auto_fill=True):
#     font = QtGui.QFont()
#     if family:
#         font.setFamily(family)
#     font.setPointSize(point_size)
#     widget.setFont(font)
#     widget.setAutoFillBackground(auto_fill)
#     widget.setStyleSheet(style_sheet)
#     return widget


# чисельник знаменник
# dividing in groups
# couples of subjects
# lessons per day
# lessons for teachers without  windows
# some lessons can't be with others in one day(e.g. ukrainian literature - foreign literature, ukrainian history - world history,
# algebra - geometry)

full_sch_class = {}
full_sch_teacher = {}
sbj = {}
with open(os.path.join(project_dir, 'temp_data.txt'), 'r') as f:
    data = f.read().split()

with open(data[1], 'r') as f:
    subjects = json.load(f)
    # for subject, data in subjects.items():
    #     data = {"banned_subjects": data[0], "hours": data[1]}
    #     subjects[subject] = data
    # # print(subjects)
    #
    # json.dump(subjects, f)

with open(data[0], 'r') as f:
    teachers = json.load(f)

with open(data[2], 'r') as f:
    # getting the input data for schedule
    classes = json.load(f)
    for num, content in classes.items():
        for letter, lessons in content.items():
            hours = 0
            # for lesson, data in lessons.items():
            #     data = {"hours": data[0], "teachers": data[1], "dividing_into_groups": data[2], "can_be_paired": data[3]}
            #     classes[num][letter][lesson] = data
            for data in lessons.values():
                hours += data["hours"]
            full_sch_class.update({f"{num}-{letter}": ScheduleClass(cls=f"{num}-{letter}", hours=hours)})
    # print(classes)
    # json.dump(classes, f)
    for name, hours in teachers.items():
        full_sch_teacher.update({name: ScheduleTeacher(name=name, hours=hours)})

# print([{cls.cls: cls.hours} for cls in full_sch_class.values()])
# with open('classes.json_files', 'w') as f:
#     json_files.dump([subjects, teachers, classes], f, indent=4)
# print(list(map(get_value, [[1, 2, 2], [2, 3, 3]])))
# print([subli[0] for subli in [[1, 2], [2, 3]]])

create_schedule(list(subjects.keys())[0], "5", "a")
print(full_sch_class["11-a"].hours)
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    print(full_sch_class)
    # print(full_sch_teacher)
    ui = ShowTable(full_sch_class)
    ui.show()

    app.exec_()
