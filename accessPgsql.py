#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/8 10:49
# @Author  : Deyu.Tian
# @Site    : 
# @File    : accessPgsql.py
# @Software: PyCharm Community Edition

import psycopg2
import psycopg2.extras
import pandas as pd
import config
TmpDir = config.outDir

def exportStationPGSQL():
    conn_string = "host='localhost' dbname='atmosqc' user='tdy52' password='123'"
    print "Connecting to database\n ->{}".format(conn_string)
    #get a connection, if failure it will throw exception
    conn = psycopg2.connect(conn_string)
    #connect cursor to perform queries
    #cursor = conn.cursor()
    crs = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    crs.execute("SELECT DISTINCT station FROM atmosqcmultistation")
    records = crs.fetchall()
    for rcd in records:
        print rcd
        query = "SELECT * FROM atmosqcmultistation where station='{}' order by station, datetimes".format(rcd[0])
        outputquery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(query)
        #crs.execute("SELECT * FROM atmosqcmultistation where station='{}'".format(rcd[0]))
        #data_recds = crs.fetchall()
        with open('{}/{}.csv'.format(TmpDir, rcd[0]), 'w') as f:
            crs.copy_expert(outputquery, f)
        #recds_df = pd.DataFrame(data_recds)
        #recds_df.to_csv('{}/{}.csv'.format(TmpDir, rcd))
    conn.close()
    pass

if __name__ == '__main__':
    exportStationPGSQL()