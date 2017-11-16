#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/16 16:26
# @Author  : Deyu.Tian
# @Site    :
# @File    : util.py.py
# @Software: PyCharm Community Edition
# @Function : 通用工具类，主要是基本的文件目录操作，自己根据需要删减和扩充

import os
import glob


def list_all_texts(folder, pattern='*', ext='TXT'):
    """
    列出指定目录及其子目录下的所有指定格式的文件
    :param folder: 指定目录
    :param pattern: 文件名, *是通配符
    :param ext: 文件后缀名
    :return: 所有符合要求文件的list
    """
    folder_dirs = [x[0] for x in os.walk(folder)]
    filenames = []
    for folderdir in folder_dirs:
        filenames.extend(glob.glob('{}\\{}.{}'.format(folderdir, pattern, ext)))
    return filenames
