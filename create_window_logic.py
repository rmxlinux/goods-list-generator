from create_window_ui import Ui_Create_Window
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QHeaderView, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
import pic_process
import os
import json

class RowNumberHeader(QHeaderView):
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.setSectionsClickable(False)
        self.setDefaultAlignment(Qt.AlignCenter)

    def paintSection(self, painter, rect, logicalIndex):
        painter.save()
        super().paintSection(painter, rect, logicalIndex)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawText(rect, Qt.AlignCenter, str(logicalIndex + 1))
        painter.restore()

class CreateWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None, path=None, is_edited=False):
        super().__init__(parent)
        self.ui = Ui_Create_Window()
        self.ui.setupUi(self)
        self.path = path
        self.is_edited = is_edited
        if is_edited:
            self.ui.button_new.setEnabled(False)
            self.ui.console.setText('编辑模式暂无法使用新建按钮与修改商品名称')
        self.status_init()
        self._init_table()
        self.ui.button_finish.clicked.connect(self._on_finish_clicked)
        self.ui.button_new.clicked.connect(self.new_line)
        self.ui.button_delete.clicked.connect(self.delete_line)
        rowNumberHeader = RowNumberHeader(Qt.Vertical, self.ui.tableWidget)
        self.ui.tableWidget.setVerticalHeader(rowNumberHeader)
    
    def init_row(self, l, r):
        table = self.ui.tableWidget
        for row in range(l, r):
            name_item = QTableWidgetItem('')
            table.setItem(row, 0, name_item)
            quantity_item = QTableWidgetItem('')
            table.setItem(row, 1, quantity_item)
    def countImages(self):
        if self.is_edited:
            with open('default.flf', 'rb') as f:
                raw_data = f.read()
                json_str = raw_data.decode('utf-8')
                self.data = json.loads(json_str)
            image_names = []
            count_names = {}
            b64 = {}
            for i in self.data['data']:
                image_names.append(i['name'])
                count_names[i['name']] = i['count']
                b64[i['name']] = i['base64']
            self.b64 = b64
            self.image_list = image_names
            self.count_names = count_names
            return len(image_names)
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
        image_names = []
        file_dict = {}
        try:
            for root, dirs, files in os.walk(self.path):
                for file in files:
                    file_extension = os.path.splitext(file)[1].lower()
                    if file_extension in image_extensions:
                        file_name = os.path.splitext(file)[0]
                        file_dict[file_name] = self.path + '\\' + file
                        image_names.append(file_name)
        except Exception:
            image_names = []
        self.image_list = image_names
        self.image2file = file_dict
        return len(image_names)
    def status_init(self):
        total = self.countImages()
        if not self.is_edited:
            self.statusBar().showMessage(f'当前目录: {self.path}, 共发现{total}张图片')
        else:
            self.statusBar().showMessage(f'载入文件成功, 共发现{total}张图片')
    def _init_table(self):
        table = self.ui.tableWidget
        table.setColumnWidth(0, 230)
        table.setColumnWidth(1, 70)
        table.setHorizontalHeaderLabels(['名称', '余量'])
        n = len(self.image_list)
        self.insert_lines(n - 1)
        now_row = 0
        for i in self.image_list:
            #print(i)
            item = QTableWidgetItem(i)
            table.setItem(now_row, 0, item)
            if self.is_edited:
                item.setFlags(item.flags() & ~(1 << 1))
                item2 = QTableWidgetItem(str(self.count_names[i]))
                table.setItem(now_row, 1, item2)
            now_row += 1

    def _on_finish_clicked(self):
        self.ui.statusbar.showMessage('正在编码中，请耐心等待')
        data = self.get_table_data()
        if data['ok']:
            json_str = json.dumps(data)
            binary_data = json_str.encode('utf-8')
            with open('default.flf', 'wb') as file:
                file.write(binary_data)
            self.close()
    
    def new_line(self):
        n = int(self.ui.spin_new_count.value())
        now_cnt = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.setRowCount(now_cnt + n)
        #self.init_row(now_cnt, now_cnt + n)
    def insert_lines(self, n):
        now_cnt = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.setRowCount(now_cnt + n)
        #self.init_row(now_cnt, now_cnt + n)
    def delete_line(self):
        try:
            row_num = int(self.ui.line_delete.text()) - 1
            if 0 <= row_num < self.ui.tableWidget.rowCount():
                self.ui.tableWidget.removeRow(row_num)
                self.ui.console.setText("")
            else:
                self.ui.console.setText("请输入合法的行号")
        except ValueError:
            self.ui.console.setText("请输入合法的行号")


    def get_table_data(self):
        data = {
            "data":[]
        }
        for row in range(self.ui.tableWidget.rowCount()):
            try:
                name = self.ui.tableWidget.item(row, 0).text().strip()
                quantity = self.ui.tableWidget.item(row, 1).text().strip()
            except Exception:
                self.ui.console.setText(f"保存失败：第{row + 1}行有空白内容")
                data["ok"] = 0
                data["data"] = []
                return data
            if name and quantity:
                try:
                    much = int(quantity)
                    if name not in self.image_list:
                        self.ui.console.setText(f"保存失败：第{row + 1}行的名称{name}没有对应的图片")
                        data["ok"] = 0
                        data["data"] = []
                        return data
                    if not self.is_edited:
                        data["data"].append({
                            "base64": pic_process.image2base64(self.image2file[name]),
                            "count": much,
                            "name": name
                        })
                    else:
                        data["data"].append({
                            "base64": self.b64[name],
                            "count": much,
                            "name": name
                        })

                except ValueError:
                    self.ui.console.setText(f"保存失败：第{row + 1}行余量不为整数")
                    data["ok"] = 0
                    data["data"] = []
                    return data
            else:
                self.ui.console.setText(f"保存失败：第{row + 1}行有空白内容")
                data["ok"] = 0
                data["data"] = []
                return data
        data["ok"] = 1
        return data