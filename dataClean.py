#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/13 10:55
# @Author  : Deyu.Tian
# @Site    : 
# @File    : dataClean.py
# @Software: PyCharm Community Edition

import pandas as pd
import numpy as np

import config
tempDataDir = '{}\\temperture'.format(config.obsvDataDir)

tempDF = pd.read_table('{}/SURF_CLI_CHN_MUL_DAY-TEM-12001-196001.TXT'.format(tempDataDir), sep='\s+',
                   usecols=[0, 4, 5, 6, 8, 9], names=['stationID', 'year', 'month', 'day', 'maxDayTemp', 'minDayTemp'],
                   dtype={'stationID': np.string0, 'maxDayTemp': np.float32, 'minDayTemp': np.float32}, parse_dates=[[1,2,3]])

def data_clean():
    pass