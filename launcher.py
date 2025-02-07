import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from main_window_ui import Ui_MainWindow
from create_window_logic import CreateWindow
from option_window_logic import OptionWindow
from about_window_logic import AboutWindow
from help_window_logic import HelpWindow
import traceback
import os

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.Button_Open.clicked.connect(self.open_file)
        self.ui.Button_Save.clicked.connect(self.save_file)
        self.ui.Button_Create.clicked.connect(self.open_folder)
        self.ui.Button_Generate.clicked.connect(self.generate)
        self.ui.button_about.clicked.connect(self.open_about_window)
        self.ui.button_help.clicked.connect(self.open_help_window)
        self.is_edited = False
        
    def open_create_window(self,path,is_edited):
        self.create_window = CreateWindow(parent=self,path=path,is_edited=is_edited)
        self.create_window.show()
    def open_option_window(self,path):
        self.option_window = OptionWindow(parent=self,path=path)
        self.option_window.show()
    def open_about_window(self):
        self.about_window = AboutWindow(parent=self)
        self.about_window.show()
    def open_help_window(self):
        self.help_window = HelpWindow(parent=self)
        self.help_window.show()

    def open_folder(self):
        if self.is_edited:
            self.open_create_window(path=None, is_edited=self.is_edited)
            return
        folder_path = QFileDialog.getExistingDirectory(self, "选择素材图片所在文件夹")
        if(folder_path) :
            self.open_create_window(path=folder_path, is_edited=self.is_edited)
            self.is_edited = True
            self.ui.Button_Create.setText('编辑')
            self.ui.statusbar.showMessage('新建谷团成功，可以生成图片')
    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, '选择谷团文件', '', '谷团数据文件 (*.flf)')
        if(file_path) :
            self.is_edited = True
            self.ui.Button_Create.setText('编辑')
            escape_path = file_path.replace('/', '\\')
            os.system(f"copy \"{escape_path}\" default.flf")
            self.ui.statusbar.showMessage('载入成功，可以进行编辑')
    def save_file(self):
        if not self.is_edited:
            self.ui.statusbar.showMessage(f'您还没有新建或打开谷团文件！')
            return
        file_path, _ = QFileDialog.getSaveFileName(self, '保存谷团文件', '', '谷团数据文件 (*.flf)')
        os.system(f'copy default.flf \"{file_path}\"')
        self.ui.statusbar.showMessage(f'文件已保存到{file_path}')

    def generate(self):
        file_path, _ = QFileDialog.getSaveFileName(self, '保存余量图片', '', '图片文件 (*.png)')
        if file_path:
            self.open_option_window(path=file_path)
        else:
            self.ui.statusbar.showMessage(f'未选取文件')

if __name__ == "__main__":
    try:
        app = QtWidgets.QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        error_info = traceback.format_exc()
        QMessageBox.critical(self, '错误：请将此窗口的截图发至dandinking@buaa.edu.cn', f'{e}\n\n{error_info}')
