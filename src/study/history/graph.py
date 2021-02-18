# -*- coding: utf-8 -*-


import matplotlib.pyplot as plt
import pandas as pd
import datetime
import numpy as np
import file_cache as fc
import mplfinance as mpf
import matplotlib as mpl# 用于设置曲线参数
from collections import OrderedDict

mpl.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
mpl.rcParams['axes.unicode_minus']=False #用来正常显示负号


def draw():
    pass

def get_style():
    mc = mpf.make_marketcolors(
        up='red', 
        down='green', 
        edge='i', 
        wick='i', 
        volume='in', 
        inherit=True)
    
    style = mpf.make_mpf_style(base_mpl_style="ggplot", marketcolors=mc)
    return style

def boll(df):
    window=20
    df["avg20"]=df["Close"].rolling(window,min_periods=0).mean()
    std=df["Close"].rolling(window,min_periods=0).std()
    df["stress"]=df["avg20"]+2*std
    df["support"]=df["avg20"]-2*std
    features=df[["Close","avg20","stress","support"]]
#     plt.show()
    tline=list(df["support"].dropna().to_dict(OrderedDict).items())
    print(tline)
#     fig,ax0=plt.subplots(1,1)
#     mpf.plot(df, type="candle",mav=(10,20) , title=df.at[df.index[-1],"名称"],style=get_style(), volume=True,figscale=5)
    mpf.plot(df, type="candle",mav=(20) , style=get_style(), figscale=5,alines={"alines":tline, "colors":"blue"},volume=True)
    
#     features.plot(grid=True,ax=ax0)
    plt.show()

def convert_cname(df):
    df.rename(columns={'收盘价':'Close', '开盘价':'Open', '最高价':'High',"最低价":"Low",'成交量': 'Volume'}, inplace = True)
    df.sort_index(inplace=True)
    df=df[-200:]
#     print(df.at[df.index[-1],"名称"])
    
#     mpf.plot(df, type="candle",mav=(10) , title=df.at[df.index[-1],"名称"],style=get_style(), volume=True,figscale=5)
    

csi500 = pd.read_csv("000905.csv", encoding="gbk",index_col=0,parse_dates=[0])

convert_cname(csi500)
boll(csi500[-100:])
    
    
    
#     print(recent)
# test()
# for ind in len(range(inflow):

