import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

class ClickableLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # 获取标签内容（文字）的矩形区域
            text_rect = self.contentsRect()
            # 判断鼠标点击位置是否在文字区域内
            if text_rect.contains(event.pos()):
                print("标签内的文字被左键点击了")
        super().mousePressEvent(event)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # 创建自定义的可点击标签
        label = ClickableLabel("点击我")
        layout.addWidget(label)

        self.setLayout(layout)
        self.setWindowTitle("可点击的 QLabel")
        self.setGeometry(300, 300, 300, 200)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())