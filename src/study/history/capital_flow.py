# -*- coding: utf-8 -*-


import matplotlib.pyplot as plt
import pandas as pd
import file_cache as fc
import datetime

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

csi500 = pd.read_csv("study\\history\\000905_20210131.csv", encoding="gbk")
# csi500 = fc.get_from_cache("csi500")
csi500.index = pd.to_datetime(csi500.pop("日期"), format='%Y-%m-%d')
csi500 = csi500.sort_index(ascending=False)[:103]
csi500 = csi500[["收盘价", "开盘价", "最高价"]]
print(csi500)
csi500fc = fc.get_from_cache("csi500cf")


csi500fc.index = pd.to_datetime(csi500fc.pop("日期"), format='%Y-%m-%d')
# print(csi500fc)

inflow = csi500fc[csi500fc["主力净流入净额"].str.contains("-") == False][["主力净流入净额"]]
print("inflow ", inflow)



xx=[]
yy=[]

guess1 = csi500[csi500["开盘价"] == csi500["最高价"]]
csi500.pop("最高价")
open=csi500.pop("开盘价")
csi500.plot(grid=True)
for i, row in inflow.iterrows():

    if i not in csi500.index:
        print(str(i)[:10], " not in df")
        continue
    xx.append(i)
    # ind1 = str(i + datetime.timedelta(days=1))[:10]
    # xx1.append(ind1)
    # yy1.append(csi500.loc[ind1, "开盘价"])
    y = csi500.loc[i, "收盘价"]
    yy.append(y)
    plt.annotate(row["主力净流入净额"],
                 xy=(i, y)
                 )



    print("index:", i)
    print("data:", row["主力净流入净额"])



plt.scatter(xx, yy, c = 'r', marker = 'o')



xx1 = [x+datetime.timedelta(days=1) for x in xx if x+datetime.timedelta(days=1) in open.index]
print(xx1)
yy1 = [open.loc[x] for x in xx1]
print(yy1)
plt.scatter(xx1, yy1, c="b", marker="x")
plt.show()

# for ind in len(range(inflow):

