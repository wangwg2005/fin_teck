# -*- coding: utf-8 -*-


import matplotlib.pyplot as plt
import pandas as pd
import datetime

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

csi500 = pd.read_csv("study\\history\\000905_20210131.csv", encoding="gbk")
# csi500 = fc.get_from_cache("csi500")
csi500.index = pd.to_datetime(csi500.pop("日期"), format='%Y-%m-%d')
csi500 = csi500.sort_index()
csi500 = csi500[["收盘价"]]


csi500["涨跌"] = csi500["收盘价"].diff() > 0

hash_vals = []
hash = 0
mask = (1 << 10) - 1
print(bin(mask))
for val in csi500["涨跌"].tolist():

    hash_vals.append(hash)
    hash = int(hash << 1)
    hash = (hash | int(val)) & mask


hash_vals
keys = set(hash_vals)
dict = [(key, hash_vals.count(key)) for key in keys ]
df = pd.DataFrame(data=dict,columns=["key", "cnt"])
df = df.sort_values(by="cnt", ascending=False)
print(df)
csi500["hash1"] = hash_vals


# print(csi500)
# for ind in len(range(inflow):

