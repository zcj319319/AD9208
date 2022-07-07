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

import numpy
from PyQt5 import QtWidgets
import random

from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from numpy import array
from AD9802 import Ui_MainWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
import matlab.engine
import matlab
import matplotlib.pyplot as plt

from matlab_file.plot_file import f_flip
from run_main.pragh_paint import config_info, param_info

engine = matlab.engine.start_matlab()  # 启动matlab


class LoadingPanel(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # self.po_annotation = []
        self.setupUi(self)
        self.init_param()
        # self.x = []
        # self.y = []
        # self.ind = []
        # self.init()
        # self.mag_all = None
        # self.index_SIG1 = None
        # self.index_SIG2 = None
        # self.figure.canvas.mpl_connect('scroll_event', self.scroll)
        # self.figure.canvas.mpl_connect('motion_notify_event', self.on_move)
        # self.run_btn.clicked.connect(self.drawing_pic)
        # self.reset_btn.clicked.connect(self.reset_pic)
        self.file_toolButton.clicked.connect(self.openFile)
        self.run_btn.clicked.connect(self.run_project)
        self.config_transfer = {}
        self.param_transfer = {}

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


    def init_param(self):
        self.sample_rate_txt.setText('3e9')
        self.smpBitsMode_txt.setText('256')
        self.sectNum_txt.setText('16')
        self.sectBits_txt.setText('32')
        self.wordBits_txt.setText('8')
        self.memoryVol_txt.setText('65536')
        # self.sigbw_input.setText('100e6')
        # self.dpdbw_input.setText('300e6')
        # self.sideband_input.setText('3000')
        # self.sideband_sig_input.setText('10e6')
        # self.fullscale_input.setText('1200')
        # self.Rl_input.setText('100')
        # self.num_interleave_input.setText('4')
        # self.num_HD_input.setText('5')
        # self.num_IMD_input.setText('5')
        # self.window_input.setText('hann')
        # self.nyquitst_zone_input.setText('2')
        # self.dacOSR_input.setText('1')
        # self.plot_range_input.setText('0')
        # self.dbc_th_HD_input.setText('-20')
        # self.dbc_th_IMD_input.setText('-20')
        # self.dbc_th_IL_input.setText('-20')
        # self.dbc_th_SFDR_input.setText('-20')
        # self.ENOB_include_HD_input.setText('0')
        # self.plot_option_input.setText('1')
        self.figure_overwrite_input.setText('1')
        # self.refclk_ratio_input.setText('1')
        # self.sig_angle_input.setText('0')
        # self.dc_1f_noise_cancel_input.setText('20e6')

    def check_param(self):
        self.config_transfer = {}
        self.param_transfer = {}
        config = config_info()
        if self.sample_rate_txt.text().strip(" ") == '':
            self.config_transfer['sample_rate'] = float(config.sample_rate)
        else:
            self.config_transfer['sample_rate'] = float(self.sample_rate_txt.text().strip(" "))
        if self.smpBitsMode_txt.text().strip(" ") == '':
            self.config_transfer['smpBitsMode'] = float(config.smpBitsMode)
        else:
            self.config_transfer['smpBitsMode'] = float(self.smpBitsMode_txt.text().strip(" "))
        if self.sectNum_txt.text().strip(" ") == '':
            self.config_transfer['sectNum'] = float(config.sectNum)
        else:
            self.config_transfer['sectNum'] = float(self.sectNum_txt.text().strip(" "))
        if self.sectBits_txt.text().strip(" ") == '':
            self.config_transfer['sectBits'] = float(config.sectBits)
        else:
            self.config_transfer['sectBits'] = float(self.sectBits_txt.text().strip(" "))
        if self.wordBits_txt.text().strip(" ") == '':
            self.config_transfer['wordBits'] = float(config.wordBits)
        else:
            self.config_transfer['wordBits'] = float(self.wordBits_txt.text().strip(" "))
        if self.memoryVol_txt.text().strip(" ")=='':
            self.config_transfer['memoryVol'] = float(config.memoryVol)
        else:
            self.config_transfer['memoryVol'] = float(self.memoryVol_txt.text().strip(" "))

        if self.sigbw_input.text().strip(" ") == '':
            pass
        else:
            self.param_transfer['sigbw'] = float(self.sigbw_input.text().strip(" "))
        if self.dpdbw_input.text().strip(" ") == '':
            pass
        else:
            self.param_transfer['dpdbw'] = float(self.dpdbw_input.text().strip(" "))
        if self.sideband_input.text().strip(" ") == '':
            pass
        else:
            self.param_transfer['sideband'] = float(self.sideband_input.text().strip(" "))
        if self.sideband_sig_input.text().strip(" ") == '':
            pass
        else:
            self.param_transfer['sideband_sig'] = float(self.sideband_sig_input.text().strip(" "))
        if self.fullscale_input.text().strip(" ") == '':
            pass
        else:
            self.param_transfer['fullscale'] = float(self.fullscale_input.text().strip(" "))
        if self.Rl_input.text().strip(" ") == '':
            pass
        else:
            self.param_transfer['Rl'] = float(self.Rl_input.text().strip(" "))
        if self.num_interleave_input.text().strip(" ") == '':
            pass
        else:
            self.param_transfer['num_interleave'] = float(self.num_interleave_input.text().strip(" "))
        if self.num_HD_input.text().strip(" ") == '':
            pass
        else:
            self.param_transfer['num_HD'] = float(self.num_HD_input.text().strip(" "))
        if self.num_IMD_input.text().strip(" ") == '':
            pass
        else:
            self.param_transfer['num_IMD'] = float(self.num_IMD_input.text().strip(" "))
        if self.window_input.text().strip(" ") == '':
            pass
        else:
            self.param_transfer['window'] = self.window_input.text().strip(" ")
        if self.nyquitst_zone_input.text().strip(" ") == '':
            pass
        else:
            self.param_transfer['nyquitst_zone'] = float(self.nyquitst_zone_input.text().strip(" "))
        if self.dacOSR_input.text().strip(" ") == '':
            pass
        else:
            self.param_transfer['dacOSR'] = float(self.dacOSR_input.text().strip(" "))
        if self.plot_range_input.text().strip(" ") == '':
            pass
        else:
            self.param_transfer['plot_range'] = float(self.plot_range_input.text().strip(" "))
        if self.dbc_th_HD_input.text().strip(" ") == '':
            pass
        else:
            self.param_transfer['dbc_th_HD'] = float(self.dbc_th_HD_input.text().strip(" "))
        if self.dbc_th_IMD_input.text().strip(" ") == '':
            pass
        else:
            self.param_transfer['dbc_th_IMD'] = float(self.dbc_th_IMD_input.text().strip(" "))
        if self.dbc_th_IL_input.text().strip(" ") == '':
            pass
        else:
            self.param_transfer['dbc_th_IL'] = float(self.dbc_th_IL_input.text().strip(" "))
        if self.dbc_th_SFDR_input.text().strip(" ") == '':
            pass
        else:
            self.param_transfer['dbc_th_SFDR'] = float(self.dbc_th_SFDR_input.text().strip(" "))
        if self.ENOB_include_HD_input.text().strip(" ") == '':
            pass
        else:
            self.param_transfer['ENOB_include_HD'] = float(self.ENOB_include_HD_input.text().strip(" "))
        if self.plot_option_input.text().strip(" ") == '':
            pass
        else:
            self.param_transfer['plot_option'] = float(self.plot_option_input.text().strip(" "))
        if self.figure_overwrite_input.text().strip(" ") == '':
            pass
        else:
            self.param_transfer['figure_overwrite'] = float(self.figure_overwrite_input.text().strip(" "))
        self.param_transfer['imd_mode'] = float(self.imd_mode_cmbox.currentText())
        if self.refclk_ratio_input.text().strip(" ") == '':
            pass
        else:
            self.param_transfer['refclk_ratio'] = float(self.refclk_ratio_input.text().strip(" "))
        if self.sig_angle_input.text().strip(" ") == '':
            pass
        else:
            self.param_transfer['sig_angle'] = float(self.sig_angle_input.text().strip(" "))
        if self.dc_1f_noise_cancel_input.text().strip(" ") == '':
            pass
        else:
            self.param_transfer['dc_1f_noise_cancel'] = float(self.dc_1f_noise_cancel_input.text().strip(" "))

    def openFile(self):
        curPath = QDir.currentPath()
        file_path, f_type = QFileDialog.getOpenFileName(self, 'choose a File', curPath,
                                                        'All Files (*);;Text Files (*.txt)')
        if len(file_path) != 0:
            self.file_path_lineinput.setText(file_path)
        else:
            return

    def run_project(self):
        global xrange, yrange
        if len(self.file_path_lineinput.text()) == 0:
            QMessageBox.information(self, 'warning', 'please input file!')
        else:
            # try:
            # plt.cla()
            # plt.xlabel('Frequency (Hz)')
            # plt.ylabel('Amplitude (dB)')
            self.check_param()
            pref = engine.memory_data_analyze(self.file_path_lineinput.text(), self.config_transfer, self.param_transfer)
            # self.mag_all = pref['mag_all']
            # self.index_SIG1 = pref['index_SIG1']
            # if pref['plot_range'] != 0:
            #     plot_range = min(pref['plot_range'], pref['dacOSR'])
            #     xrange = [x / pref['N_fft'] * pref['fs'] + (pref['nq'] - 1) / 2 * pref['fs'] / pref['dacOSR'] for x
            #               in range(0, int(pref['N_nq'] * pref['plot_range'] / 2))]
            #     yrange = [pref['mag_full'][j] for j in
            #               f_flip([y for y in range(1, int((pref['N_nq'] * plot_range) / 2) + 1)], pref['nq'])]
            #     yrange = array(yrange)
            #     yrange = [20 * math.log10(yrange[i]) for i in range(0, len(yrange))]
            # elif pref['plot_range'] == 0:
            #     xrange = [x / pref['N_fft'] * pref['fs'] + (pref['nq'] - 1) / 2 * pref['fs'] for x in
            #               range(0, int(pref['N_fft'] / 2))]
            #     yrange = [pref['mag_full'][j] for j in
            #               f_flip([y for y in range(1, int(pref['N_fft'] / 2 + 1))], pref['nq'])]
            #     yrange = array(yrange)
            #     yrange = [20 * math.log10(yrange[i]) for i in range(0, len(yrange))]
            # self.ax.plot(xrange, yrange, color='gray')
            # plt.grid(True)
            # # self.mark_plot_figure(pref)
            # plt.xlim(xrange[1], xrange[-1])
            # plt.yticks(numpy.arange(-150, 90, step=10))
            # self.canvas.draw_idle()
            # # except Exception as e:
            # #     print(e)

    def mark_plot_figure(self, pref):
    #     sig
        sig_ind = pref['sig_ind']
        sig_yrange = pref['sig_yrange']
        self.ax.plot(array(sig_ind)[0],numpy.transpose(array(sig_yrange))[0],color='blue')
        if pref['imd_mode']==1:
            imd_mode_ind= pref['imd_mode_ind']
            imd_mode_yrange=pref['imd_mode_yrange']
            self.ax.plot(imd_mode_ind[0],numpy.transpose(array(imd_mode_yrange))[0],color='blue')
        # if 'sigbw' in self.param_transfer.keys():
        #     sigbw = pref['sigbw']
        #     self.ax.plot()
        num_HD = pref['num_HD']
        num_IMD = pref['num_IMD']
        disable_HD_SIG1 = pref['disable_HD_SIG1']
        for i in range(1,int(num_HD)):
            if disable_HD_SIG1[0][i-1]!=1:
                HD_ind = pref['HD_ind']
                HD_yrange = pref['HD_yrange']
                self.ax.plot(array(HD_ind)[0],numpy.transpose(array(HD_yrange))[0],'r--')
        # if pref['imd_mode']==1:
        #     for i in range(2,int(num_HD)):
        #         print(array(disable_HD_SIG1))
        #         if array(disable_HD_SIG1)[0][i-1]!=1:
        #             imd_mode_HD_ind = pref['imd_mode_HD_ind']
        #             imd_mode_HD_yrange = pref['imd_mode_HD_yrange']
        #             self.ax.plot(imd_mode_HD_ind,imd_mode_HD_yrange,'r--')
        #     for n in range(2,num_IMD+1):
        #         for k in range(1,2*(n-1)+1):
        #             if pref['disable_IMD'](n-1,k)!=1:
        #                 num_IMD_ind = pref['num_IMD_ind']
        #                 num_IMD_yrange = pref['num_IMD_yrange']
        #                 self.ax.plot(num_IMD_ind,num_IMD_yrange,'r--')
        num_interleave = pref['num_interleave']
        if int(num_interleave) !=1:
            for n in range(1,len(pref['index_center_IL_OS'])+1):
                if pref['disable_IL_OS'](n)!=1:
                    os_ind = pref['os_ind']
                    os_yrange = pref['os_yrange']
                    self.ax.plot(os_ind,os_yrange,'g')
            index_center_IL_GTS_SIG1 = pref['index_center_IL_GTS_SIG1']
            disable_IL_GTS_SIG1 = pref['disable_IL_GTS_SIG1']
            for n in range(1,len(index_center_IL_GTS_SIG1)+1):
                if disable_IL_GTS_SIG1(n)!=1:
                    gain_ind = pref['gain_ind']
                    gain_yrange = pref['gain_yrange']
                    self.ax.plot(gain_ind,gain_yrange,'m')
            index_center_IL_GTS_SIG2 = pref['index_center_IL_GTS_SIG2']
            disable_IL_GTS_SIG2 = pref['disable_IL_GTS_SIG2']
            if pref['imd_mode']==1:
                for n in range(1,len(index_center_IL_GTS_SIG2)+1):
                    if disable_IL_GTS_SIG2(n)!=1:
                        gain_imd_mode_ind = pref['gain_imd_mode_ind']
                        gain_imd_mode_yrange = pref['gain_imd_mode_yrange']
                        self.ax.plot(gain_imd_mode_ind,gain_imd_mode_yrange,'m')
        refclk_ratio = pref['refclk_ratio']
        if refclk_ratio!=1:
            for n in range(1,len(pref['index_center_REF_SPUR_SIG1'])+1):
                if pref['disable_REF_SPUR_SIG1'](n)!=1:
                    refclk_ratio_ind = pref['refclk_ratio_ind']
                    refclk_ratio_yrange = pref['refclk_ratio_yrange']
                    self.ax.plot(refclk_ratio_ind,refclk_ratio_yrange,'r')
        index_center_REF_SPUR_SIG2 = pref['index_center_REF_SPUR_SIG2']
        disable_REF_SPUR_SIG2 = pref['disable_REF_SPUR_SIG2']
        if pref['imd_mode']==1:
            for n in range(1,len(index_center_REF_SPUR_SIG2)+1):
                if disable_REF_SPUR_SIG2(n)!=1:
                    refclk_ratio_imd_mode_ind =pref['refclk_ratio_imd_mode_ind']
                    refclk_ratio_imd_mode_yrange = pref['refclk_ratio_imd_mode_yrange']
                    self.ax.plot(refclk_ratio_imd_mode_ind,refclk_ratio_imd_mode_yrange)
        spur_ind = pref['spur_ind']
        spur_yrange = pref['spur_yrange']
        self.ax.plot(spur_ind,spur_yrange)


    # def result_display(self,pref):
    #     if pref['imd_mode']==1:
    #


    def reset_result(self):
        pass


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
