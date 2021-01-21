# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import pandas as pd
import math

csi500 = pd.read_csv("000905.csv", encoding="gbk")


csi500["roll_max"]=csi500["收盘价"].rolling(window=10).max()
csi500["raise"]=csi500["roll_max"]/csi500["收盘价"]-1
# print(csi500[["收盘价","roll_max","raise"]])
date_time = pd.to_datetime(csi500.pop('日期'), format='%Y-%m-%d')
csi500.index=date_time


# csi500["shadow"]= min(csi500["开盘价"], csi500["收盘价"]) - csi500["最低价"]
df=csi500[["开盘价","收盘价"]]
df["min1"]=df.min(axis=1)
df["shadow"]=df["min1"]-csi500["最低价"]
df["raise1"]=csi500["raise"]
df["high"]=csi500["最高价"]
df=df[df.shadow>100]
print("shadow bigger than 100,",len(df))
dft=df[df.raise1>0.05]
print("return over 5%",len(dft))
dft=df[df.raise1==0]
print("return is 0%",len(dft))
df1=df.sort_values(by="raise1", ascending=False)
df1=df1[(df.shadow>df.high - df.min1)]
df1.plot.scatter(x='shadow' , y='raise1')
plt.show()
print(df1[["raise1","shadow"]])