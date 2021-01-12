# -*- coding: utf-8 -*-

import pandas as pd
import math
import matplotlib.pyplot as plt

leve_csi500 = pd.read_excel("融资融券中证500.xls",header=1, encoding="gbk")
# leve_csi300 = pd.read_excel("融资融券沪深300.xls",header=1, encoding="gbk")
leve_total = pd.read_excel("融资融券全市场.xls",header=1, encoding="gbk")

price_csi500=pd.read_csv("000905.csv",encoding="gbk")

 
len=min(len(leve_csi500),len(leve_total),len(price_csi500))
# len=1200
 
def mode_std(b):
    a = b - 800
    return 3000*math.cos(a/60-0.55)+5000+80*math.cos(a/5 *math.pi)

 
features=pd.DataFrame()

date_time = pd.to_datetime(price_csi500.pop('日期'), format='%Y-%m-%d')
price_csi500.index=date_time

date_time = pd.to_datetime(leve_csi500.pop('交易日期'), format='%Y-%m-%d')
leve_csi500.index=date_time

date_time = pd.to_datetime(leve_total.pop('日期'), format='%Y-%m-%d')
leve_total.index=date_time

features["price"]=price_csi500["收盘价"]
features["融资余额500"]=leve_csi500["融资余额(亿元)"]
features["融资余额"]=leve_total["融资余额(亿元)"]
features["risk1"]=series1=(features["price"]-1000-features["融资余额500"])*2
# features["risk2"]=series1=(2.7*features["price"]-1000-features["融资余额"])*2
features.plot(grid=True)

plt.show()
