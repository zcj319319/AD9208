#!/usr/bin/env python 
# -*- coding: utf-8 -*-
'''
Time    : 2022/06/30 9:18
Author  : zhuchunjin
Email   : chunjin.zhu@taurentech.net
File    : sql_opeartion.py
Software: PyCharm
'''
import sqlite3


class database:
    def __init__(self):
        self.conn = sqlite3.connect("AD9802dbTrace.db",check_same_thread=False)
        # 创建游标
        self.cursor = self.conn.cursor()

