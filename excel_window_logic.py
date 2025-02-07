from excel_window_ui import Ui_Excel_Window
from mode_window_ui import Ui_Mode_Window
from match_window_ui import Ui_match_window
from create_window_logic import CreateWindow
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QHeaderView, QVBoxLayout, QLabel, QHBoxLayout, QWidget, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage
import pic_process
import pandas
import os
import json
import sip

class ModeWindow(QtWidgets.QMainWindow):
    mode_selected = pyqtSignal(int)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Mode_Window()
        self.ui.setupUi(self)
        self.ui.radio_folder.setChecked(True)
        self.ui.pushButton.clicked.connect(self.feedback)

    def feedback(self):
        if self.ui.radio_folder.isChecked():
            self.mode = 0
        elif self.ui.radio_auto_1.isChecked():
            self.mode = 1
        elif self.ui.radio_auto_2.isChecked():
            self.mode = 2
        self.mode_selected.emit(self.mode) 
        self.close()

class ClickableQLabel(QLabel):
    clicked = pyqtSignal(int, int, str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setAlignment(Qt.AlignCenter)
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            x = event.pos().x()
            y = event.pos().y()
            self.clicked.emit(x, y, self.objectName())
        if not sip.isdeleted(self):
            super().mousePressEvent(event)

class MatchWindow(QtWidgets.QMainWindow):
    saved = pyqtSignal(list)
    def __init__(self, parent, name_list, file_list, is_matched, name2count):
        super().__init__(parent)
        self.ui = Ui_match_window()
        self.ui.setupUi(self)
        self.name_list = name_list
        self.file_list = file_list
        self.is_matched = is_matched
        self.name_index = 0
        self.name2count = name2count
        self.data_append = []
        self.show_name()

    def show_name(self):
        i = self.name_index
        if i >= len(self.name_list):
            self.saved.emit(self.data_append)
            self.close()
            return
        self.ui.label_pic.setText(f'<html><head/><body><p><span style=" font-size:14pt; font-weight:700;">{self.name_list[i]}</span></p></body></html>')
        main_layout = QVBoxLayout()
        current_row_layout = QHBoxLayout()
        current_row_width = 0
        self.target_width = 100

        for image_path in self.file_list:
            if self.is_matched[image_path]:
                continue
            pixmap = QPixmap(image_path)
            scaled_pixmap = pixmap.scaledToWidth(self.target_width, Qt.SmoothTransformation)
            label = ClickableQLabel(self)
            label.setObjectName(image_path)
            label.setPixmap(scaled_pixmap)
            current_row_width += self.target_width
            if current_row_width > self.ui.scroll_options.width():
                main_layout.addLayout(current_row_layout)
                current_row_layout = QHBoxLayout()
                current_row_width = self.target_width
            label.clicked.connect(self.picked)
            current_row_layout.addWidget(label)
        main_layout.addLayout(current_row_layout)
        content_widget = QWidget()
        content_widget.setLayout(main_layout)
        self.ui.scroll_options.setWidget(content_widget)

    def picked(self, x, y, ObjectName):
        self.is_matched[ObjectName] = True
        self.data_append.append({
            "base64": pic_process.image2base64(ObjectName),
            "count": self.name2count[self.name_list[self.name_index]],
            "name": self.name_list[self.name_index]
        })
        self.name_index += 1
        self.show_name()
        

class ExcelWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None, path=None):
        super().__init__(parent)
        self.ui = Ui_Excel_Window()
        self.ui.setupUi(self)
        self.path = path
        self.ui.pushButton.clicked.connect(self.ana_excel)

    def str2pos(self,sstr):
        letter = ""
        x_id = ""
        for c in sstr:
            if c.isalpha():
                letter += c
            elif c.isdigit():
                x_id += c
        y = 0
        if (not letter) or (not x_id):
            return -1, -1
        for i, l in enumerate(reversed(letter)):
            y += (ord(letter) - 64) * (26 ** i)
        return (int(x_id) - 1), (y - 1)

    def ana_excel(self):
        try:
            excel_file = pandas.ExcelFile(self.path)
            sheet = excel_file.parse(0,header=None)
            #print(len(sheet))
        except Exception:
            self.ui.statusBar.showMessage('文件格式错误，不是有效的excel文件' + self.path)
            return
        #read the names
        name_b = self.ui.name_1.text()
        name_e = self.ui.name_2.text()
        if (not name_b) or (not name_e):
            self.ui.statusBar.showMessage('不可输入空白内容')
            return
        name_b_x, name_b_y = self.str2pos(name_b)
        name_e_x, name_e_y = self.str2pos(name_e)
        if name_b_x < 0 or name_b_y < 0 or name_e_x < 0 or name_e_y < 0:
            self.ui.statusBar.showMessage('输入内容不合法')
            return
        name_list = []
        for i in range(name_b_x, name_e_x + 1):
            for j in range(name_b_y, name_e_y + 1):
                #print(str(sheet.iloc[i, j]))
                try:
                    if(str(sheet.iloc[i, j]) not in name_list):
                        name_list.append(str(sheet.iloc[i, j]))
                    else:
                        self.ui.statusBar.showMessage(f'表格中 {str(sheet.iloc[i, j])} 一项重复')
                        return
                except IndexError:
                    self.ui.statusBar.showMessage('选择的名称区域超出了表格实际大小')
                    return
        #read the counts
        count_b = self.ui.count_1.text()
        count_e = self.ui.count_2.text()
        if (not count_b) or (not count_e):
            self.ui.statusBar.showMessage('不可输入空白内容')
            return
        count_b_x, count_b_y = self.str2pos(count_b)
        count_e_x, count_e_y = self.str2pos(count_e)
        if count_b_x < 0 or count_b_y < 0 or count_e_x < 0 or count_e_y < 0:
            self.ui.statusBar.showMessage('输入内容不合法')
            return
        name2count = {}
        pos = 0
        for i in range(count_b_x, count_e_x + 1):
            for j in range(count_b_y, count_e_y + 1):
                if pos >= len(name_list):
                    break
                try:
                    name2count[name_list[pos]] = int(sheet.iloc[i, j])
                    pos += 1
                except ValueError:
                    self.ui.statusBar.showMessage('选择的余量区域中含有非数字内容')
                    return
                except IndexError:
                    self.ui.statusBar.showMessage('选择的余量区域超出了表格实际大小')
                    return
            if pos >= len(name_list):
                break
        if pos < len(name_list):
            for i in range(pos, len(name_list)):
                name2count[name_list[pos]] = 0
        #save to default.flf, then commit default.flf to create window
        self.name_list = name_list
        self.name2count = name2count
        self.mode_window = ModeWindow(self)
        self.mode_window.mode_selected.connect(self.save_flf)
        self.mode_window.show()

    def save_flf(self, mode):
        self.close()
        self.mode_window.close()
        self.mode = mode
        self.file_list = []
        self.is_matched = {}
        self.find_names = []
        if self.mode == 0:
            folder_path = QFileDialog.getExistingDirectory(self, "选择素材图片所在文件夹")
            if(folder_path) :
                image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
                data = {"data":[]}
                #print(self.name_list)
                files_total = []
                for root, dirs, files in os.walk(folder_path):
                    files_total += files
                #print(self.name_list)
                for char_name in self.name_list:
                    #print(char_name)
                    for file in files_total:
                        file_extension = os.path.splitext(file)[1].lower()
                        if file_extension in image_extensions:
                            file_name = os.path.splitext(file)[0]
                            file_path = folder_path + '/' + file
                            if file_path in self.is_matched:
                                if self.is_matched[file_path]:
                                    continue
                            self.file_list.append(file_path)
                            if file_name == char_name:   
                                #print(f"succeed, matched {file_path} to {file_name}")
                                self.is_matched[file_path] = True
                                data["data"].append({
                                    "base64": pic_process.image2base64(file_path),
                                    "count": self.name2count[file_name],
                                    "name": file_name
                                })
                                self.find_names.append(char_name)
                                break
                            else:
                                #print(f"failed to match {file_path} , file name is {file_name}, char name is {char_name}")
                                if file_path not in self.is_matched:
                                    self.is_matched[file_path] = False
            self.data = data
            #print(self.find_names)
            #print(self.name_list)
            if len(self.find_names) < len(self.name_list):
                to_find = []
                for char_name in self.name_list:
                    if char_name not in self.find_names:
                        to_find.append(char_name)
                #print(to_find)
                self.match_window = MatchWindow(self, to_find, self.file_list, self.is_matched, self.name2count)
                self.match_window.show()
                self.match_window.saved.connect(self.save_op)
            else:
                self.save_op([])

    def save_op(self, data_append):
        self.data["data"] += data_append
        json_str = json.dumps(self.data)
        binary_data = json_str.encode('utf-8')
        with open('default.flf', 'wb') as file:
            file.write(binary_data)
        self.create_window = CreateWindow(self, path=None, is_edited=True)
        self.create_window.show()
