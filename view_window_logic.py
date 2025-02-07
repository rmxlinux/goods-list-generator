import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from PIL import Image
import view_window_ui

class ViewWindow(QtWidgets.QMainWindow):
    def __init__(self, image, parent=None):
        super().__init__(parent)
        self.ui = view_window_ui.Ui_view_window()
        self.ui.setupUi(self)
        width, height = image.size
        if width > 1000:
            new_height = int(height * (1000 / width))
            image = image.resize((1000, new_height), Image.Resampling.LANCZOS)
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        self.data = image.tobytes('raw', 'RGBA')
        qimage = QImage(self.data, image.size[0], image.size[1], QImage.Format_RGBA8888)
        
        pixmap = QPixmap.fromImage(qimage)
        self.ui.statusbar.hide()
        self.resize(pixmap.width(), pixmap.height())
        self.ui.label.setScaledContents(True)
        self.ui.label.resize(pixmap.width(), pixmap.height())
        self.ui.label.setPixmap(pixmap)