# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import pandas as pd

csi500 = pd.read_csv("000905.csv", encoding="gbk")
# csi300 = pd.read_csv("000300.csv", encoding="gbk")
# 
# len=min(len(csi300),len(csi500))
# 
csi500=csi500[:1000]
# csi300=csi300[:len]
# 
# features=pd.DataFrame()
# features["沪深300"]=csi300["收盘价"]
# features["中证500"]=csi500["收盘价"]
# 
# # features["csi500"]=csi500["收盘价"]
# # features["csi300"]=features.pop("收盘价")
# date_time = pd.to_datetime(csi500.pop('日期'), format='%Y-%m-%d')
# features.index=date_time
# print(features)
# features.plot(grid=True)
# 
# plt.show()
# date_time = pd.to_datetime(csi300.pop('日期'), format='%Y-%m-%d')
# csi300.index=date_time

# 
# csi500=csi500[:1000]
csi500 = csi500.reindex(index=csi500.index[::-1])
# csi500.index=range(len(csi500))
csi500["no"]=range(len(csi500))
date_time = pd.to_datetime(csi500.pop('日期'), format='%Y-%m-%d')
csi500.index=date_time
# plt.show()

print(csi500[["收盘价","no"]])

reflect = 6200

import math
 
delta = len(csi500)-800
 
def mode_1(b):
    a = b - delta
    return 650*math.cos(a/60-0.29)+5750+80*math.cos(a/5 *math.pi)
 
def mode_2(a):
#     a = b - delta
    return 1125*math.cos(a/160+math.pi/2-0.1)+5600+80*math.cos(a/5 *math.pi)

def mode_long_term(b):
    a = b - delta
    return 1125*math.cos(a/160+math.pi/2-0.1)+5200+80*math.cos(a/5 *math.pi)

def mode_std(b):
    a = b - delta
    return 3000*math.cos(a/60-0.55)+5000+80*math.cos(a/5 *math.pi)

 
# features = csi500[["收盘价"]]
# features["sim"] = list(map(mode_long_term, range(len(csi500))))
features=pd.DataFrame()

features.plot(grid=True)
plt.show()
