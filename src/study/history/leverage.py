# -*- coding: utf-8 -*-


import matplotlib.pyplot as plt
import pandas as pd


def read(filename):
    df = pd.read_excel("融资融券"+filename+"_all_latest.xls",header=1, encoding="gbk")
    return df



# filenames=["全市场","沪深300","中证500","上证50"]
filenames=["沪深300","中证500","创业"]

dfs=list(map(read,filenames))
# csi500 = pd.read_excel("融资融券中证500.xls",header=1, encoding="gbk")
# csi300 = pd.read_excel("融资融券沪深300.xls",header=1, encoding="gbk")
# total = pd.read_excel("融资融券.xls",header=1, encoding="gbk")
 
len_df=min(list(map(len,dfs)))
# len=1200
 
dfs=list(map(lambda df:df[:len_df],dfs))
# csi500=csi500[:len]
# csi300=csi300[:len]

rz=True
rq=False
all=False
 
features=pd.DataFrame()

if all:
    for i in range(len(filenames)):    
        features[filenames[i]+"融资融券"]=dfs[i]["融资融券余额(亿元)"]
#     features["全市场融资融券"]=total["融资融券余额(亿元)"]
#     features["沪深300融资融券"]=csi300["融资融券余额(亿元)"]
#     features["中证500融资融券"]=csi500["融资融券余额(亿元)"]
#     features["融资融券diff"]=csi500["融资融券余额(亿元)"]-csi300["融资融券余额(亿元)"]

if rz:
    for i in range(len(filenames)):
        features[filenames[i]+"融资"]=dfs[i]["融资余额(亿元)"]
#     features["全市场融资"]=total["融资余额(亿元)"]
#     features["沪深300融资"]=csi300["融资余额(亿元)"]
#     features["中证500融资"]=csi500["融资余额(亿元)"]
features["融资diff"]=-features["中证500融资"]+features["沪深300融资"]

if rq:
    for i in range(len(filenames)): 
       features[filenames[i]+"融资"]=dfs[i]["融券余额(亿元)"]
 
# features["csi500"]=csi500["收盘价"]
# features["csi300"]=features.pop("收盘价")
features=features[:len_df]
date_time = pd.to_datetime(dfs[1].pop('交易日期'), format='%Y-%m-%d')
# print(len(date_time))
features.index=date_time[:len_df]
# features=features[1200 : 1600]
print(features)
features.plot(grid=True)
plt.show()