# -*- coding: utf-8 -*-


import matplotlib.pyplot as plt
import pandas as pd
import file_cache as fc

# csi500 = pd.read_csv("study\\history\\000905.csv", encoding="gbk")
csi500 = fc.get_from_cache("csi500")
csi500.index = pd.to_datetime(csi500.pop("日期"), format='%Y-%m-%d')
# csi500=csi500[["收盘价"]]
# print(csi500)
csi500fc = fc.get_from_cache("csi500cf")


csi500fc.index = pd.to_datetime(csi500fc.pop("日期"), format='%Y-%m-%d')
# print(csi500fc)

inflow = csi500fc[csi500fc["主力净流入净额"].str.contains("-") == False][["主力净流入净额"]]
print("inflow ", inflow)

csi500.plot(grid=True)

xx=[]
yy=[]

for i, row in inflow.iterrows():
    if str(i)[:10] not in csi500.index:
        print(str(i)[:10] , " not in df")
        continue
    xx.append(i)
    yy.append(csi500.loc[str(i)[:10], "中证500"])
    plt.annotate(row["主力净流入净额"],
                 xy=(i, csi500.loc[str(i)[:10], "中证500"])
                 )

    print("index:", i)
    print("data:", row["主力净流入净额"])

plt.scatter(xx,yy,c = 'r',marker = 'o')
plt.show()

# for ind in len(range(inflow):

