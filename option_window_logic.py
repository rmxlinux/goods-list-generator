from option_window_ui import Ui_option_window
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QColorDialog, QVBoxLayout, QPushButton
import pic_generator
import view_window_logic
from PyQt5.QtGui import QIcon, QPixmap

class OptionWindow(QtWidgets.QMainWindow):
    def __init__(self,parent=None, path=None):
        super().__init__(parent)
        self.ui = Ui_option_window()
        self.ui.setupUi(self)
        self.ui.button_modify.clicked.connect(self.open_color_dialog)
        self.ui.button_OK.clicked.connect(self.generate)
        self.ui.button_view.clicked.connect(self.view)
        self.path = path
        options = ["样式1", "样式2", "样式3"]
        image_paths = ["banned_1.png", "banned_2.png", "banned_3.png"]
        for option, image_path in zip(options, image_paths):
            pixmap = QPixmap(image_path)
            icon = QIcon(pixmap)
            self.ui.comboBox.addItem(icon, option)
        font_options = ["times.ttf", "arial.ttf", "msyh.ttc"]
        font_paths = ["times.png", "arial.png", "msyh.png"]
        for option, path in zip(font_options, font_paths):
            pixmap = QPixmap(path)
            icon = QIcon(pixmap)
            self.ui.comboBox_2.addItem(icon, option)

    def open_color_dialog(self):
        color = QColorDialog.getColor()
        if color.isValid():
            r, g, b = color.red(), color.green(), color.blue()
            self.ui.r_text.setText(str(r))
            self.ui.g_text.setText(str(g))
            self.ui.b_text.setText(str(b))
    
    def update(self):
        try:
            r, g, b = int(self.ui.r_text.text()), int(self.ui.g_text.text()), int(self.ui.b_text.text())
        except ValueError:
            self.ui.statusbar.showMessage('请将颜色值设置为[0,255]以内的整数')
            return False
        if not ((0 <= r <= 255) and (0 <= g <= 255) and (0 <= b <=255)):
            self.ui.statusbar.showMessage('请将颜色值设置为[0,255]以内的整数')
            return False
        self.t_color = (r, g, b)
        try:
            self.w_limit = int(self.ui.max_width.text())
            if self.w_limit < 0:
                self.w_limit = 1926081700
        except ValueError:
            self.ui.statusbar.showMessage('最大图片宽度不为整数')
            return False
        try:
            self.reduce = float(self.ui.reduction.text())
            if self.reduce < 0:
                self.ui.statusbar.showMessage('缩小倍率小于0')
                return False
        except ValueError:
            self.ui.statusbar.showMessage('缩小倍率不为有效的小数')
            return False
        txtCombo = self.ui.comboBox.currentText()
        self.fonts = self.ui.comboBox_2.currentText()
        if txtCombo.find('1') != -1:
            self.imgtype = 'banned_1.png'
        elif txtCombo.find('2') != -1:
            self.imgtype = 'banned_2.png'
        elif txtCombo.find('3') != -1:
            self.imgtype = 'banned_3.png'
        return True
    
    def generate(self):
        if self.update():
            self.close()
            pic_generator.generate(path=self.path, w_limit=self.w_limit, text_color=self.t_color, banned_img=self.imgtype, fonts=self.fonts, reduction=self.reduce)

    def view(self):
        if self.update():
            pic = pic_generator.generate(path='~return', w_limit=self.w_limit, text_color=self.t_color, banned_img=self.imgtype, fonts=self.fonts, reduction=self.reduce)
            view_window = view_window_logic.ViewWindow(parent=self,image=pic)
            view_window.show()

        
