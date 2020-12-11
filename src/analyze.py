# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

import pandas as pd

ind300=pd.read_csv(r"C:\Users\Darren\eclipse-workspace\fin_study\src\000300_20201128.csv",encoding="gbk")
ind500=pd.read_csv(r"C:\Users\Darren\eclipse-workspace\fin_study\src\000905_20201128.csv",encoding="gbk")

date_time = pd.to_datetime(ind300.pop('日期'), format='%Y-%m-%d')
date_time2 = pd.to_datetime(ind500.pop('日期'), format='%Y-%m-%d')
range=-1

close300=ind300["收盘价"][:range]
# close300.rename(index=str,columns={"收盘价":"沪深300"})
close500=ind500["收盘价"][:range]
plot_features =pd.concat( [close300,close500],axis=1)
plot_features.columns=["沪深300","中证500"]
plot_features.index = date_time[:range]
# ind300.index=date_time
# print(ind300)
plot_features.plot()
plt.show()


