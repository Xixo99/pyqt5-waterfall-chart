import math
import sys
import time
from random import randint, random

import numpy as np

from matplotlib import pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDateTime, QObject, Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QBrush, QColor, QPen
from PyQt5.QtWidgets import (QApplication, QDialog, QLabel, QLineEdit,
                             QMainWindow, QVBoxLayout, QWidget)

from QCustomPlot2 import *

from ui.upchart import Ui_Form      # 使用QtDesigner将ui转为py文件，从外部导入作为界面


class MainWidow(QMainWindow, Ui_Form):
    def __init__(self):
        super(MainWidow, self).__init__()
        self.setupUi(self)          # setupUi方法写在Ui_Form类中

        self.pushButton.clicked.connect(self.setTime)
        self.pushButton_2.clicked.connect(self.getData)

        self.timer = QTimer()       # 定义计时器
        self.timer.timeout.connect(self.getData)
        self.is_running = False
        self.log_value = []
        self.newdata = np.zeros(200)
        self.scale = 200

    '''方法实现区'''

    def setTime(self):
        if self.is_running:
            self.timer.stop()
            self.is_running = False
        else:
            self.timer.start(200)
            self.is_running = True

    def getData(self):
        self.newdata = np.random.randint(0, 255, self.scale)
        self.log_value.insert(0, self.newdata)   # 随即生成新的随机向量模拟新到来数据
        if len(self.log_value) > 50:
            # 只缓存最新的50条数据
            self.log_value.pop()

        # 更新数据后绘图
        self.drawLineChart()
        self.drawWaterfall()

    def drawLineChart(self):
        customPlot = self.linechart
        customPlot.clearGraphs()

        # 添加一些交互功能，拖拽图像，缩放，选择曲线
        customPlot.setInteractions(QCP.Interactions(
            QCP.iRangeDrag | QCP.iRangeZoom | QCP.iSelectPlottables))
        # 添加绘图图像
        graph = customPlot.addGraph()
        # 设置绘图颜色
        graph.setPen(QPen(Qt.blue))
        graph.setBrush(QBrush(QColor(0, 0, 255, 20)))  # brush可以填充曲线与横轴所夹的面积

        # 添加数据
        graph.setData(range(self.scale), self.newdata)
        # chart.replot()
        customPlot.rescaleAxes()  # 自动设置坐标轴范围及刻度
        customPlot.replot()

    def drawWaterfall(self):
        customPlot = self.fallchart
        # 添加一些交互功能，拖拽图像，缩放，选择曲线
        customPlot.setInteractions(QCP.Interactions(
            QCP.iRangeDrag | QCP.iRangeZoom | QCP.iSelectPlottables))
        self.colorMap = QCPColorMap(customPlot.xAxis, customPlot.yAxis)
        self.colorMap.data().setSize(200, 50)
        self.colorMap.data().setRange(QCPRange(0, 1024), QCPRange(0, 100))

        for i in range(len(self.log_value)):
            row_vec = self.log_value[i]
            for j in range(row_vec.size):
                self.colorMap.data().setCell(
                    j, 49-i, row_vec[j])  # 根据生成的数据，逐个单元调整颜色深度
        self.colorMap.rescaleDataRange(True)
        customPlot.rescaleAxes()
        customPlot.replot()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = MainWidow()
    form.show()
    sys.exit(app.exec_())
