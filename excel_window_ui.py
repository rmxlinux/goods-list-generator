# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'excel_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Excel_Window(object):
    def setupUi(self, Excel_Window):
        Excel_Window.setObjectName("Excel_Window")
        Excel_Window.resize(322, 347)
        self.centralwidget = QtWidgets.QWidget(Excel_Window)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 20, 81, 41))
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.name_1 = QtWidgets.QLineEdit(self.centralwidget)
        self.name_1.setGeometry(QtCore.QRect(90, 20, 51, 20))
        self.name_1.setText("")
        self.name_1.setObjectName("name_1")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(150, 20, 41, 41))
        self.label_2.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.name_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.name_2.setGeometry(QtCore.QRect(210, 20, 51, 20))
        self.name_2.setText("")
        self.name_2.setObjectName("name_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 80, 81, 41))
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.count_1 = QtWidgets.QLineEdit(self.centralwidget)
        self.count_1.setGeometry(QtCore.QRect(90, 80, 51, 20))
        self.count_1.setText("")
        self.count_1.setObjectName("count_1")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(150, 80, 41, 41))
        self.label_4.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.count_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.count_2.setGeometry(QtCore.QRect(210, 80, 51, 20))
        self.count_2.setText("")
        self.count_2.setObjectName("count_2")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(20, 130, 291, 151))
        self.label_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_5.setWordWrap(True)
        self.label_5.setObjectName("label_5")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 290, 291, 31))
        self.pushButton.setObjectName("pushButton")
        Excel_Window.setCentralWidget(self.centralwidget)
        self.statusBar = QtWidgets.QStatusBar(Excel_Window)
        self.statusBar.setObjectName("statusBar")
        Excel_Window.setStatusBar(self.statusBar)

        self.retranslateUi(Excel_Window)
        QtCore.QMetaObject.connectSlotsByName(Excel_Window)

    def retranslateUi(self, Excel_Window):
        _translate = QtCore.QCoreApplication.translate
        Excel_Window.setWindowTitle(_translate("Excel_Window", "选择表格区域"))
        self.label.setText(_translate("Excel_Window", "名称数据从"))
        self.label_2.setText(_translate("Excel_Window", "到"))
        self.label_3.setText(_translate("Excel_Window", "余量数据从"))
        self.label_4.setText(_translate("Excel_Window", "到"))
        self.label_5.setText(_translate("Excel_Window", "<html><head/><body><p>例：从 A1 到 A19</p><p><span style=\" color:#ff0000;\">注：暂时只能选择Sheet1中的内容。</span></p><p><span style=\" color:#ff0000;\">推荐将数据排列为一列，若选择范围为矩形，则会按从左到右，从上到下的顺序匹配。</span></p><p><span style=\" color:#ff0000;\">优先匹配名称，若没有匹配的余量数据则默认余量为0。</span></p></body></html>"))
        self.pushButton.setText(_translate("Excel_Window", "确定"))
