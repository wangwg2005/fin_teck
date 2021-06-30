# -*- coding: utf-8 -*-
import datetime
from study.leverage import time_util as tutil
from study.leverage import leverage_reader as lreader
import pandas as pd

ttoday=datetime.date.today()

pre_day=tutil.get_prevous_trade_date(ttoday)

pre2_day=tutil.get_prevous_trade_date(pre_day)


def analyze_sse():

    pre_day_str=tutil.stringfy(pre_day)
    df1=lreader.read_detail_sse(pre_day_str)
    
    pre2_day_str=tutil.stringfy(pre2_day)
    df2=lreader.read_detail_sse(pre2_day_str)
    
    
    df=df1[["标的证券简称"]]
    df[pre_day_str]=df1["本日融资余额(元)"]
    df[pre2_day_str]=df2["本日融资余额(元)"]
    
    df["incr"]=df[pre_day_str]/df[pre2_day_str]-1
    df["quant"]=df[pre_day_str]-df[pre2_day_str]
    
    dfn=df.sort_values(by=['incr'],ascending=False)
    
    print(dfn.head(20))
    
    dfn2=df.sort_values(by=['quant'],ascending=False)
    
    print(dfn2.head(20))
    
def convert_number(a):
    return int(a.replace(",",""))
    
def analyze_szse():
    pre_day_str=str(pre_day)
    df1=lreader.read_detail_szse(pre_day_str)
    
    pre2_day_str=str(pre2_day)
    df2=lreader.read_detail_szse(pre2_day_str)
    
    
    df=df1[["证券简称"]]
    df[pre_day_str]=df1["融资余额(元)"].map(convert_number)
    df[pre2_day_str]=df2["融资余额(元)"].map(convert_number)
    
    df["incr"]=df[pre_day_str]/df[pre2_day_str]-1
    df["quant"]=df[pre_day_str]-df[pre2_day_str]
    
    dfn=df.sort_values(by=['incr'],ascending=False)
    
    print(dfn.head(20))
    
    dfn2=df.sort_values(by=['quant'],ascending=False)
    
    print(dfn2.head(20))

analyze_szse()