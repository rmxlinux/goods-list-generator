from help_window_ui import Ui_help_window
from PyQt5 import QtWidgets, QtCore, QtGui

class HelpWindow(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.ui = Ui_help_window()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.accept)

    def accept(self):
        self.close()