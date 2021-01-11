# -*- coding: utf-8 -*-

import pandas as pd
import math

leve_csi500 = pd.read_excel("融资融券中证500.xls",header=1, encoding="gbk")
# leve_csi300 = pd.read_excel("融资融券沪深300.xls",header=1, encoding="gbk")
leve_total = pd.read_excel("融资融券.xls",header=1, encoding="gbk")

price_csi500=pd.read_csv("000905.csv",encoding="gbk")
 
len=min(len(leve_csi500),len(leve_total),len(price_csi500))
# len=1200
 
def mode_std(b):
    a = b - 800
    return 3000*math.cos(a/60-0.55)+5000+80*math.cos(a/5 *math.pi)

 
features=pd.DataFrame()

features["price"]=price_csi500["收盘价"]
features["model1"]=price_csi500["收盘价"]
