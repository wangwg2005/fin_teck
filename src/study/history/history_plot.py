# -*- coding: utf-8 -*-


import matplotlib.pyplot as plt
import pandas as pd

csi500 = pd.read_csv("000905.csv", encoding="gbk")
csi300 = pd.read_csv("000300.csv", encoding="gbk")

len=min(len(csi300),len(csi500))
# len=1000
 
csi500=csi500[:len]
csi300=csi300[:len]
 
features=pd.DataFrame()
features["沪深300"]=csi300["收盘价"]
features["中证500"]=csi500["收盘价"]
features["diff"]=csi500["收盘价"]-csi300["收盘价"]
 
# features["csi500"]=csi500["收盘价"]
# features["csi300"]=features.pop("收盘价")
date_time = pd.to_datetime(csi500.pop('日期'), format='%Y-%m-%d')
features.index=date_time
# features=features[::10]
print(features)
features.plot(grid=True)
plt.show()