# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import pandas as pd
import math

csi500 = pd.read_csv("000905.csv", encoding="gbk")


def test1():
    csi500["roll_max"]=csi500["收盘价"].rolling(window=10).max()
    csi500["roll_min"]=csi500["收盘价"].rolling(window=10).min()
    csi500["raise"]=csi500["roll_max"]/csi500["收盘价"]-1
    csi500["lose"]=1-csi500["roll_min"]/csi500["收盘价"]
    # print(csi500[["收盘价","roll_max","raise"]])
    date_time = pd.to_datetime(csi500.pop('日期'), format='%Y-%m-%d')
    csi500.index=date_time
    
    
    # csi500["shadow"]= min(csi500["开盘价"], csi500["收盘价"]) - csi500["最低价"]
    df=csi500[["开盘价","收盘价","最高价","最低价","raise","lose"]]
    df["min1"]=df.min(axis=1)
    df["tall"]=df["最高价"]-csi500["最低价"]
    df["tall1"]=(df["收盘价"]-df["开盘价"]).abs()
    df["shadow_rate"]=df["tall"]/df["tall1"]
    df["valotility"]=df[["raise","lose"]].max(axis=1)
    df["high"]=csi500["最高价"]
    df=df[df.shadow_rate>100]
    print("shadow bigger than 100,",len(df))
    dft=df
    print("return over 5%",len(dft))
#     dft=df[df.raise1==0]
    print("return is 0%",len(dft))
#     df1=df.sort_values(by="raise1", ascending=False)
#     df1=df1[(df.shadow>df.high - df.min1)]
    dft.plot.scatter(x='shadow_rate' , y='valotility')
    plt.show()
    print(dft[["valotility","shadow_rate"]])
    
    
def test2():
    csi500["close_raise"]=csi500["收盘价"]/csi500["收盘价"].shift(-1)-1
    csi500["low_raise"]=csi500["最低价"]/csi500["收盘价"].shift(-1)-1
    print(csi500[["日期","收盘价","close_raise","low_raise"]])
    features=csi500[csi500.low_raise<-0.017]
#     features=csi500
    plt.scatter(features["low_raise"], features["close_raise"])
    plt.show()
    
    
test1()