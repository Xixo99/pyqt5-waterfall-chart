# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

# 注意，其中两个用于绘图的QWidget窗口提升为了QCustomPlot2 中的QCustomPlot

from QCustomPlot2 import QCustomPlot
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1283, 889)
        Form.setAutoFillBackground(True)
        self.label = QtWidgets.QLabel(Form)
        self.label.setEnabled(True)
        self.label.setGeometry(QtCore.QRect(460, 100, 496, 36))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.log = QtWidgets.QLabel(Form)
        self.log.setGeometry(QtCore.QRect(210, 60, 151, 151))
        self.log.setText("")
        self.log.setPixmap(QtGui.QPixmap("F:/图片/保存的图片/科大校徽1.jpg"))
        self.log.setScaledContents(True)
        self.log.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignHCenter)
        self.log.setObjectName("log")
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(460, 220, 511, 541))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.linechart = QCustomPlot(self.layoutWidget)
        self.linechart.setObjectName("linechart")
        self.verticalLayout.addWidget(self.linechart)
        self.fallchart = QCustomPlot(self.layoutWidget)
        self.fallchart.setObjectName("fallchart")
        self.verticalLayout.addWidget(self.fallchart)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(230, 360, 93, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(230, 300, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate(
            "Form", "Deep Learning Signal Classifier"))
        self.pushButton.setText(_translate("Form", "开始采集"))
        self.pushButton_2.setText(_translate("Form", "单次调试"))
