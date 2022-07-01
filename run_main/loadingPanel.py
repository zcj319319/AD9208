#!/usr/bin/env python 
# -*- coding: utf-8 -*-
'''
Time    : 2022/06/28 9:41
Author  : zhuchunjin
Email   : chunjin.zhu@taurentech.net
File    : loadingPanel.py
Software: PyCharm
'''
import math

from PyQt5 import QtWidgets
import random
from AD9802 import Ui_MainWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
import matlab.engine
import matplotlib.pyplot as plt

engine = matlab.engine.start_matlab()  # 启动matlab


class LoadingPanel(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.po_annotation = []
        self.setupUi(self)
        self.x = []
        self.y = []
        self.ind = []
        self.init()
        self.figure.canvas.mpl_connect('scroll_event', self.scroll)
        self.figure.canvas.mpl_connect('motion_notify_event', self.on_move)
        self.run_btn.clicked.connect(self.drawing_pic)
        self.reset_btn.clicked.connect(self.reset_pic)

    def init(self):
        self.figure = plt.figure(facecolor='gray', dpi=80)
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.horizontal_graph = QtWidgets.QVBoxLayout(self.fft_gragh)
        plt.xlabel('Frequency (MHz)')
        plt.ylabel('Amplitude (dBFS)')
        self.mpl_toolbar = NavigationToolbar(self.canvas, self)  # 创建工具条
        self.horizontal_graph.addWidget(self.mpl_toolbar)
        self.horizontal_graph.addWidget(self.canvas)

    def drawing_pic(self):
        plt.cla()
        plt.xlabel('Frequency (MHz)')
        plt.ylabel('Amplitude (dBFS)')
        [self.x, self.y] = engine.myfunc(nargout=2)
        self.ax.plot(self.x[0], self.y[0])
        self.icon_insert()
        plt.grid(True)
        self.canvas.draw_idle()

    def icon_insert(self):
        # 标注点的坐标
        self.ind = [random.randint(0, 200) for i in range(30)]
        for i in range(len(self.ind)):
            point_x = self.x[0][self.ind[i]]
            point_y = self.y[0][self.ind[i]]
            text = 'x=%s,y=%s' % (str(point_x), str(point_y))
            point, = plt.plot(point_x, point_y, 'x', c='firebrick')
            # 标注框偏移量
            offset1 = 40
            offset2 = 40
            # 标注框
            bbox1 = dict(boxstyle="round", fc='lightgreen', alpha=0.6)
            # 标注箭头
            arrowprops1 = dict(arrowstyle="->", connectionstyle="arc3,rad=0.")
            # 标注
            annotation = plt.annotate(text, xy=(point_x, point_y), xytext=(-offset1, offset2),
                                      textcoords='offset points',
                                      bbox=bbox1, arrowprops=arrowprops1, size=15)
            # 默认鼠标未指向时不显示标注信息
            annotation.set_visible(False)
            self.po_annotation.append([point, annotation])

    def reset_pic(self):
        plt.cla()
        plt.xlabel('Frequency (MHz)')
        plt.ylabel('Amplitude (dBFS)')
        self.canvas.draw_idle()

    def scroll(self, event):
        axtemp = event.inaxes
        x_min, x_max = axtemp.get_xlim()
        fanwei_x = (x_max - x_min) / 10
        if event.button == 'up':
            axtemp.set(xlim=(x_min + fanwei_x, x_max - fanwei_x))
        elif event.button == 'down':
            axtemp.set(xlim=(x_min - fanwei_x, x_max + fanwei_x))
        self.canvas.draw_idle()

    # 定义鼠标响应函数
    def on_move(self, event):
        visibility_changed = False
        for point, annotation in self.po_annotation:
            should_be_visible = (point.contains(event)[0] == True)

            if should_be_visible != annotation.get_visible():
                visibility_changed = True
                annotation.set_visible(should_be_visible)

        if visibility_changed:
            plt.draw()
