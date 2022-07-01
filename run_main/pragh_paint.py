#!/usr/bin/env python 
# -*- coding: utf-8 -*-
'''
Time    : 2022/07/01 17:37
Author  : zhuchunjin
Email   : chunjin.zhu@taurentech.net
File    : pragh_paint.py
Software: PyCharm
'''

class config_info:
    def __init__(self):
        self.smpBitsMode = 256
        self.sectNum = 16
        self.sectBits = 32
        self.wordBits = 8
        self.memoryVol = 2**16

class param_info:
    def __init__(self):
        self.sigbw = 100e6
        self.dpdbw = 300e6
        self.sideband = 3000
        self.sideband_sig = 10e6
        self.fullscale = 1200
        self.Rl = 100
        self.num_interleave = 4
        self.num_HD = 5
        self.window = 'hann'
        self.nyquitst_zone = 2
        self.dacOSR = 1
        self.imd_mode = 1
        self.plot_range = 0
        self.simple_plot = 0
        self.dc_1f_noise_cancel = 20e6
        self.dbc_th_HD = -20
        self.dbc_th_IMD = -20
        self.dbc_th_IL = -20
        self.dbc_th_SFDR = -20

def paint_widget(handle):
    pass