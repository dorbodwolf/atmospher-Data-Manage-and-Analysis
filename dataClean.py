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
tempDir = '{}\\temperture'.format(config.obsvDataDir)
precDir = '{}\\preciption'.format(config.obsvDataDir)
evapDir = '{}\\evaporation'.format(config.obsvDataDir)
surfDir = '{}\\surfaceTemp'.format(config.obsvDataDir)
windDir = '{}\\windSpeed'.format(config.obsvDataDir)

resultDir = '{}'.format(config.resultDataDir)

from util import *
TEMPS = list_all_texts(tempDir)
PRECS = list_all_texts(precDir)
EVAPS = list_all_texts(evapDir)
SURFS = list_all_texts(surfDir)
WINDS = list_all_texts(windDir)
ATMOS = [TEMPS, PRECS]


def _post_processing(atmos):
    """
    对合并后表格后处理
    :return: 处理后的表格
    """
    atmos.columns = ['year_month_day', 'stationID', 'maxDayTemp', 'minDayTemp', '_year_month_day', '_stationID',
                     'accumPrec']
    atmos['accumPrec_1'] = atmos['accumPrec']
    atmos['accumPrec_1'] = pd.to_numeric(atmos['accumPrec_1'], errors='coerce')
    atmos['year'] = atmos['year_month_day'].dt.year
    atmos['month'] = atmos['year_month_day'].dt.month
    atmos['day'] = atmos['year_month_day'].dt.day
    cols = atmos.columns.tolist()
    #print(cols)
    cols = [cols[1]] + cols[-3:] + [cols[-4]] + cols[2:7] + [cols[0]]
    atmos = atmos[cols]
    for index, row in atmos.iterrows():
        atmos.loc[index, 'maxDayTemp'] = row['maxDayTemp'] * 0.1
        atmos.loc[index, 'minDayTemp'] = row['minDayTemp'] * 0.1
        if row['accumPrec_1'] == 32700:
            atmos.loc[index, 'accumPrec_1'] = 0
        elif row['accumPrec_1'] >= 32000 and row['accumPrec_1'] < 32700:
            atmos.loc[index, 'accumPrec_1'] = (row['accumPrec_1'] - 32000) * 0.1
        elif row['accumPrec_1'] >= 31000 and row['accumPrec_1'] < 32000:
            atmos.loc[index, 'accumPrec_1'] = (row['accumPrec_1'] - 31000) * 0.1
        elif row['accumPrec_1'] >= 30000 and row['accumPrec_1'] < 31000:
            atmos.loc[index, 'accumPrec_1'] = (row['accumPrec_1'] - 30000) * 0.1
        if index > 50:
            break
    return atmos




def combine_all_files():
    temp = pd.read_table(TEMPS[0], sep='\s+', usecols=[0, 4, 5, 6, 8, 9],
                         names=['stationID', 'year', 'month', 'day', 'maxDayTemp', 'minDayTemp'],
                         dtype={'stationID': np.string0, 'maxDayTemp': np.float32, 'minDayTemp': np.float32},
                         parse_dates=[[1, 2, 3]])
    prec = pd.read_table(PRECS[0], sep='\s+', usecols=[0, 4, 5, 6, 9],
                         names=['stationID', 'year', 'month', 'day', 'accumPrec'],
                         dtype={'stationID': np.string0, 'accumPrec': np.int32}, parse_dates=[[1, 2, 3]])
    atmos = pd.concat([temp, prec], axis=1)
    for i in range(len(ATMOS)): #2
        for j in range(1, len(ATMOS[i])): #48
            if i == 0:
                tempe = pd.read_table(TEMPS[j], sep='\s+', usecols=[0, 4, 5, 6, 8, 9],
                                        names=['stationID', 'year', 'month', 'day', 'maxDayTemp', 'minDayTemp'],
                                        dtype={'stationID': np.string0, 'maxDayTemp': np.float32,
                                               'minDayTemp': np.float32}, parse_dates=[[1, 2, 3]])
                temp = pd.concat([temp, tempe])
            if i == 1:
                prece = pd.read_table(PRECS[j], sep='\s+', usecols=[0, 4, 5, 6, 9],
                                     names=['stationID', 'year', 'month', 'day', 'accumPrec'],
                                     dtype={'stationID': np.string0, 'accumPrec': np.int32}, parse_dates=[[1, 2, 3]])
                prec = pd.concat([prec, prece])
    atmose = pd.concat([temp, prec], axis=1)
    atmos = pd.concat([atmos, atmose])
    atmos = _post_processing(atmos)
    return atmos

if __name__ == '__main__':
    atmos = combine_all_files()
    atmos.to_csv('{}\\atmos.csv'.format(resultDir))