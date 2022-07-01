#!/usr/bin/env python 
# -*- coding: utf-8 -*-
'''
Time    : 2022/06/28 9:37
Author  : zhuchunjin
Email   : chunjin.zhu@taurentech.net
File    : Run_main.py
Software: PyCharm
'''

import sys

from PyQt5 import QtWidgets

from run_main.loadingPanel import LoadingPanel

app = QtWidgets.QApplication(sys.argv)

if __name__ == '__main__':
    try:
        ex = LoadingPanel()
        ex.show()
        sys.exit(app.exec_())
    except Exception as e:
        raise e
