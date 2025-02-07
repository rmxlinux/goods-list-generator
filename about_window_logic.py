from about_window_ui import Ui_AboutWindow
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap

class AboutWindow(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.ui = Ui_AboutWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.accept)
        pixmap = QPixmap('icon_b.png')
        self.ui.label_2.setPixmap(pixmap)
        self.ui.label_2.setScaledContents(True)

    def accept(self):
        self.close()