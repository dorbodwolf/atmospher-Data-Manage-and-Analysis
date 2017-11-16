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

from util import *
TEMPS = list_all_texts(tempDir)
PRECS = list_all_texts(precDir)
EVAPS = list_all_texts(evapDir)
SURFS = list_all_texts(surfDir)
WINDS = list_all_texts(windDir)
ATMOS = [TEMPS, PRECS]



def split_stations():
    """
    拆分站点
    :return: 返回的站点数据集合
    """
    atmos_panda = combine_all_files()
    pass




def combine_all_files():
    temp = pd.read_table(TEMPS[0], sep='\s+', usecols=[0, 4, 5, 6, 8, 9],
                         names=['stationID', 'year', 'month', 'day', 'maxDayTemp', 'minDayTemp'],
                         dtype={'stationID': np.string0, 'maxDayTemp': np.float32, 'minDayTemp': np.float32},
                         parse_dates=[[1, 2, 3]])
    prec = pd.read_table(PRECS[0], sep='\s+', usecols=[0, 4, 5, 6, 9],
                         names=['stationID', 'year', 'month', 'day', 'accumPrec'],
                         dtype={'stationID': np.string0, 'accumPrec': np.int32}, parse_dates=[[1, 2, 3]])
    atoms = pd.concat([temp, prec], axis=1)
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
    atomse = pd.concat([temp, prec], axis=1)
    atoms = pd.concat([atoms, atomse])
    return atoms