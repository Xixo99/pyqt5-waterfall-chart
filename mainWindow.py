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

        self.pushButton.clicked.connect(self.waveplot)
        self.pushButton_2.clicked.connect(self.waterfall)

        self.timer = QTimer()       # 定义计时器
        self.timer.timeout.connect(self.waterfall)
        self.is_running = False
        self.log_value = []

    '''方法实现区'''

    def waveplot(self):
        if self.is_running:
            self.timer.stop()
            self.is_running = False
        else:
            self.timer.start(200)
            self.is_running = True

    def waterfall(self):
        customPlot = self.fallchart
        self.colorMap = QCPColorMap(customPlot.xAxis, customPlot.yAxis)
        self.colorMap.data().setSize(200, 50)
        self.colorMap.data().setRange(QCPRange(0, 1024), QCPRange(0, 100))

        self.log_value.insert(0, np.random.randint(
            0, 255, 200))   # 随即生成新的随机向量模拟新到来数据
        if len(self.log_value) > 50:
            # 只缓存最新的50条数据
            self.log_value.pop()

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
