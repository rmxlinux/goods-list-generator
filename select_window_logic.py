from select_window_ui import Ui_Select_Window
from create_window_logic import CreateWindow
from excel_window_logic import ExcelWindow
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QHeaderView, QVBoxLayout, QWidget, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt

class SelectWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.ui = Ui_Select_Window()
        self.ui.setupUi(self)
        self.ui.radio_folder.setChecked(True)
        self.ui.pushButton.clicked.connect(self.mode_select)

    def mode_select(self):
        if self.ui.radio_folder.isChecked():
            folder_path = QFileDialog.getExistingDirectory(self, "选择素材图片所在文件夹")
            if(folder_path) :
                self.close()
                self.parent.open_create_window(path=folder_path, is_edited=False)
        elif self.ui.radio_excel.isChecked():
            file_filter = "表格文件 (*.xls *.xlsx)"
            file_path, _ = QFileDialog.getOpenFileName(self, '选择表格文件', '', file_filter)
            if file_path:
                self.excel_window = ExcelWindow(self, file_path)
                self.excel_window.show()
                self.close()


