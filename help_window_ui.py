# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'help_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_help_window(object):
    def setupUi(self, help_window):
        help_window.setObjectName("help_window")
        help_window.resize(508, 265)
        self.centralwidget = QtWidgets.QWidget(help_window)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 200, 491, 61))
        self.pushButton.setObjectName("pushButton")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 491, 161))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        help_window.setCentralWidget(self.centralwidget)

        self.retranslateUi(help_window)
        QtCore.QMetaObject.connectSlotsByName(help_window)

    def retranslateUi(self, help_window):
        _translate = QtCore.QCoreApplication.translate
        help_window.setWindowTitle(_translate("help_window", "帮助"))
        self.pushButton.setText(_translate("help_window", "确定"))
        self.label.setText(_translate("help_window", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:700;\">新建/编辑</span><span style=\" font-size:10pt;\">：新建一个谷团文件，或者编辑打开的谷团文件。</span></p><p><span style=\" font-size:10pt; color:#ff0000;\">如果是新建模式，请事先准备好一个装有所有商品图片的文件夹。</span></p><p><span style=\" font-size:10pt; font-weight:700;\">打开</span><span style=\" font-size:10pt;\">：打开已经保存的谷团数据文件。</span></p><p><span style=\" font-size:10pt; font-weight:700;\">生成图片</span><span style=\" font-size:10pt;\">：将谷团余量示意图保存为图片。</span></p><p><span style=\" font-size:10pt; font-weight:700;\">保存到文件</span><span style=\" font-size:10pt;\">：将谷团数据保存到flf文件。</span></p></body></html>"))
