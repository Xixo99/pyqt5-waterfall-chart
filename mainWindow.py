import math
import socket
import sys
import json
import time
from random import randint, random

import numpy as np
from matplotlib import pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDateTime, QObject, Qt, QThread, QTimer, pyqtSignal
from PyQt5.QtGui import QBrush, QColor, QPen
from PyQt5.QtWidgets import (QApplication, QDialog, QLabel, QLineEdit,
                             QMainWindow, QVBoxLayout, QWidget)
from QCustomPlot2 import *

from ui.udpui import Ui_MainWindow  # 使用QtDesigner将ui转为py文件，从外部导入作为界面


class MainWidow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWidow, self).__init__()
        self.setupUi(self)          # setupUi方法写在Ui_Form类中

        self.testButton.clicked.connect(self.getRandData)
        self.gifButton.clicked.connect(self.setTime)
        self.buildUDPButton.clicked.connect(self.buildUDP)
        self.breakUDPButton.clicked.connect(self.breakUDP)
        self.breakUDPButton.setEnabled(False)
        self.dataButton.clicked.connect(self.udpClient)

        self.timer = QTimer()       # 定义计时器
        self.timer.timeout.connect(self.getRandData)
        self.is_running = False
        self.log_value = []
        self.scale = 200
        self.newdata = np.zeros(self.scale)
        self.udpRecvThread = None
        self.udpClientThread = None

    '''方法实现区'''

    def buildUDP(self):
        self.buildUDPButton.setText('接收数据中...')  # 主页面按钮点击后更新按钮文本
        self.buildUDPButton.setEnabled(False)  # 将按钮设置为不可点击
        self.breakUDPButton.setEnabled(True)
        self.udpRecvThread = UDPRecvThread()
        self.udpRecvThread.recvData.connect(self.getUDPData)

    def breakUDP(self):
        if self.udpRecvThread.isRunning:
            self.udpRecvThread.kill()
        self.buildUDPButton.setText('建立UDP')  # 主页面按钮点击后更新按钮文本
        self.buildUDPButton.setEnabled(True)  # 将按钮设置为不可点击
        self.breakUDPButton.setEnabled(False)
        print("UDP连接已断开！")

    def setTime(self):
        if self.is_running:
            self.timer.stop()
            self.is_running = False
        else:
            self.timer.start(200)
            self.is_running = True

    def getUDPData(self, recvdata):
        recvdata = recvdata.split(' ')
        recvdata = map(float, recvdata)
        recvdata = np.array(list(recvdata))
        self.newdata = recvdata
        self.saveData()
        self.draw()

    def getRandData(self):
        self.newdata = np.random.randint(0, 255, self.scale)
        self.saveData()
        self.draw()

    def saveData(self):
        self.log_value.insert(0, self.newdata)   # 随即生成新的随机向量模拟新到来数据
        if len(self.log_value) > 50:
            # 只缓存最新的50条数据
            self.log_value.pop()
        self.draw()

    def draw(self):
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

    def udpClient(self):
        self.udpClientThread = UDPClientThread()


class UDPRecvThread(QThread):
    recvData = pyqtSignal(str)  # 返回信号类型为np.array

    def __init__(self):
        super().__init__()
        # 1创建套接字
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.settimeout(30)  # 设置超时(s)
        # 2.绑定一个本地端口
        self.localaddr = ("127.0.0.1", 9999)  # 必须绑定自己电脑IP和port
        self.udp_socket.bind(self.localaddr)
        self.start()

    def run(self):
        # 3.接收数据
        print("开始接受数据！")
        while 1:
            # recv_data存储元组（接收到的数据，（发送方的ip,port））
            recv_data = self.udp_socket.recvfrom(1024)
            recv_msg = recv_data[0]  # 信息内容
            # send_addr = recv_data[1]  # 信息地址
            recv_msg = recv_msg.decode("gbk")

            self.recvData.emit(recv_msg)
            QApplication.processEvents()

    def kill(self):
        self.udp_socket.close()
        self.terminate()


class UDPClientThread(QThread):
    def __init__(self):
        super().__init__()
        self.server_ip = '127.0.0.1'
        self.server_port = 9999

        self.start()
        self.rawdata = np.load("row_random_data200.npy")
        self.noise = np.random.randint(0, 30, 200) - 15

    def run(self):

        # socket.SOCK_DGRAM代表是UDP通信
        udp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_client_socket.connect((self.server_ip, self.server_port))

        data = self.rawdata + self.noise

        str_ = ' '.join(str(x) for x in data)
        udp_client_socket.send(str_.encode())

        print("数据发送成功！")
        QApplication.processEvents()
        udp_client_socket.close()
        self.terminate()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = MainWidow()
    form.show()
    sys.exit(app.exec_())
