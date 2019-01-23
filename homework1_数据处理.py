#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 23:15:34 2019

@author: yangyibing
"""

import os
os.chdir('/Users/yangyibing/Desktop/QTC2019/3_数据处理_谢昊')
import pandas as pd
import talib as ta
import matplotlib.pyplot as plt
from datetime import datetime
import talib.abstract as taab

#题目一
excelfile = pd.ExcelFile('sz50.xlsx')
data={}
for i in excelfile.sheet_names:
    raw_data=pd.read_excel('sz50.xlsx',sheet_name=i,index_col='datetime')
    data[i]=raw_data

print(data.keys())

#题目二
d_frame=pd.DataFrame(data['600036.XSHG'])
moving_average=ta.MA(d_frame.close.values, 10)
print(type(moving_average))
print(moving_average[-5:])

#题目三
p=d_frame.close
s = pd.Series(moving_average,index=p.index)
plt.figure(figsize=(15, 7))
p.plot()
s.plot()

#题目四
data=pd.read_excel('sz50.xlsx',sheetname=None, index_col='datetime')
di={}
for k,v in data.items():
    try:
        index=v.index
        di[k]=pd.Series(ta.ROCR100(v.close.values,timeperiod=5),index=index)
    except AttributeError:
        pass
df=pd.DataFrame(di)
l=df.columns.values.tolist()
for i in range(5):
    plt.plot(df[l[i]],label=l[i])
plt.legend()
plt.show()

#题目五
symbol=['600000.XSHG', '600016.XSHG', '600028.XSHG', '600029.XSHG', '600030.XSHG', \
        '600036.XSHG', '600048.XSHG', '600050.XSHG', '600100.XSHG', '600104.XSHG', \
        '600111.XSHG', '600340.XSHG', '600485.XSHG', '600518.XSHG', '600519.XSHG', \
        '600547.XSHG', '600606.XSHG', '600837.XSHG', '600887.XSHG', '600919.XSHG', \
        '600958.XSHG', '600999.XSHG', '601006.XSHG', '601088.XSHG', '601166.XSHG', \
        '601169.XSHG', '601186.XSHG', '601198.XSHG', '601211.XSHG', '601229.XSHG', \
        '601288.XSHG', '601318.XSHG', '601328.XSHG', '601336.XSHG', '601390.XSHG', \
        '601398.XSHG', '601601.XSHG', '601628.XSHG', '601668.XSHG', '601688.XSHG', \
        '601766.XSHG', '601788.XSHG', '601800.XSHG', '601818.XSHG', '601857.XSHG', \
        '601881.XSHG', '601901.XSHG', '601985.XSHG', '601988.XSHG', '601989.XSHG']
data_dict = {}
for s in symbol:
    data =  pd.read_excel('sz50.xlsx',sheetname=s, index_col='datetime')#不只是收盘价close
    data_dict[s] = data.loc['2017-01-03':'2017-11-20']
PN = pd.Panel(data_dict)
if PN.isnull().values.any():
    PN.fillna(0,inplace=True)
MI = PN.to_frame()
print(MI.head())
pn_macd = pd.Panel({name: taab.MACD(value) for name, value in PN.iteritems()})
df_macd = pn_macd.transpose(2,1,0).to_frame()
print(df_macd)
