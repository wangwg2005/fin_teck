# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import pandas as pd
from numpy import sign
from numpy import polyfit

csi500_ori = pd.read_csv("000905.csv", encoding="gbk")
# csi300 = pd.read_csv("000300.csv", encoding="gbk")
# 
# len=min(len(csi300),len(csi500))
# 
csi500=csi500_ori[:1000]

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
# date_time = pd.to_datetime(csi500.pop('日期'), format='%Y-%m-%d')
# csi500.index=date_time
# plt.show()

print(csi500[["收盘价","no"]])

reflect = 6200

import math
 
delta = len(csi500)-680

gold_ration=0.618

cycle=1000

w=2*math.pi/cycle
 
def mode_1(b):
    a = b - delta
    return 650*math.cos(a/60-0.29)+5750+80*math.cos(a/5 *math.pi)
 
def mode_2(b):
    a = b - delta
    return 1150*math.cos(a/160+math.pi/2-0.1)+5200+80*math.cos(a/5 *math.pi)

def mode_long_term(b):
    a = b - delta
    return 1150*math.cos(a*w+math.pi/2-0.1)+5600+80*math.cos(a/5 *math.pi)

def mode_std(b):
    a = b - delta
    return 3000*math.cos(a/60-0.55)+5000+80*math.cos(a/5 *math.pi)

 
features = csi500[["收盘价"]]
sim_list = list(map(mode_long_term, range(len(csi500))))
features["sim"]=sim_list
# features["shift"]= list(map(mode_long_term, range(-1,len(csi500)-1)))

price=csi500["收盘价"].tolist()
# price.reverse()
adjust=0
for i in range(len(csi500)):
    print(price[i],sim_list[i])
    sim_list[i]=sim_list[i]+ adjust
    diff=price[i]-sim_list[i]
    
#     if math.fabs(diff)>140:
#         adjust=adjust+140*sign(diff)
#     else:
    adjust=diff+adjust
                 
    
# features["adjust"]=sim_list
    


# features["csi500shift"]=shift_price
# features["sim"] =features["sim"]-( features["shift"]-features["csi500shift"])
date_time = pd.to_datetime(csi500.pop('日期'), format='%Y-%m-%d')
features.index=date_time

# features.pop("shift")
# features.pop("csi500shift")
# features=pd.DataFrame()
# sim_seri=features.pop("sim")
print(features)
features.plot(grid=True)

diff_frame=pd.DataFrame()
diff_frame["diff"]=features["收盘价"]-features["sim"]

print(diff_frame["diff"].mean())
print(diff_frame["diff"].std())

def filtera(a):
    if math.fabs(a)<93:
        return 0
    else:
        return a
    
    
# diff_frame["diff"]=diff_frame["diff"].apply(filtera )
# print(diff_frame)
# diff_frame["sum"]=diff_frame["diff"].cumsum()
# diff_frame.plot(grid=True);
plt.show()
