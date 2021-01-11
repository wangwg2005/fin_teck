# -*- coding: utf-8 -*-


import matplotlib.pyplot as plt
import pandas as pd


def read(filename, colname):
    df = pd.read_excel("融资融券"+filename+".xls",header=1, encoding="gbk")



filenames=["全市场","沪深300","中证500","上证50"]

dfs=list(map(read,filenames))
csi500 = pd.read_excel("融资融券中证500.xls",header=1, encoding="gbk")
csi300 = pd.read_excel("融资融券沪深300.xls",header=1, encoding="gbk")
total = pd.read_excel("融资融券.xls",header=1, encoding="gbk")
 
len=min(len(csi300),len(csi500),len(total))
# len=1200
 
csi500=csi500[:len]
csi300=csi300[:len]

rz=True
rq=False
all=False
 
features=pd.DataFrame()
if all:
    features["全市场融资融券"]=total["融资融券余额(亿元)"]
    features["沪深300融资融券"]=csi300["融资融券余额(亿元)"]
    features["中证500融资融券"]=csi500["融资融券余额(亿元)"]
    features["融资融券diff"]=csi500["融资融券余额(亿元)"]-csi300["融资融券余额(亿元)"]

if rz:
    features["全市场融资"]=total["融资余额(亿元)"]
    features["沪深300融资"]=csi300["融资余额(亿元)"]
    features["中证500融资"]=csi500["融资余额(亿元)"]
    features["融资diff"]=csi500["融资余额(亿元)"]-csi300["融资余额(亿元)"]

if rq:
    features["全市场融券"]=total["融券余额(亿元)"]
    features["沪深300融券"]=csi300["融券余额(亿元)"]
    features["中证500融券"]=csi500["融券余额(亿元)"]
    features["融券diff"]=csi500["融券余额(亿元)"]-csi300["融券余额(亿元)"]
 
# features["csi500"]=csi500["收盘价"]
# features["csi300"]=features.pop("收盘价")
features=features[:len]
date_time = pd.to_datetime(csi500.pop('交易日期'), format='%Y-%m-%d')
# print(len(date_time))
features.index=date_time[:len]
print(features)
features.plot(grid=True)
plt.show()