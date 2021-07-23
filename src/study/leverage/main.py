# -*- coding: utf-8 -*-
import datetime
from study.leverage import time_util as tutil
from study.leverage import leverage_reader as lreader
import pandas as pd
import matplotlib.pyplot as plt 
from pandas_datareader import data, wb

ttoday=datetime.date.today()

pre_day=tutil.get_prevous_trade_date(ttoday)

pre2_day=tutil.get_prevous_trade_date(pre_day)


def filter_sse():

    pre_day_str=tutil.stringfy(pre_day)
    df1=lreader.read_detail_sse(pre_day_str)
    
    pre2_day_str=tutil.stringfy(pre2_day)
    df2=lreader.read_detail_sse(pre2_day_str)
    
    
    df=df1[["标的证券简称"]]
    df["融资买入额(元)"]=df1["本日融资买入额(元)"]
    df=df.rename(columns={"标的证券简称":"证券简称"})
    df[pre_day_str]=df1["本日融资余额(元)"]
    df[pre2_day_str]=df2["本日融资余额(元)"]
    
    df=df.filter(regex="^60", axis=0)
    df["incr"]=df[pre_day_str]/df[pre2_day_str]-1
    df["quant"]=df[pre_day_str]-df[pre2_day_str]
    
    dfn=df.sort_values(by=['incr'],ascending=False)
    
    print(dfn.head(20))
    
    dfn2=df.sort_values(by=['quant'],ascending=False)
    
    print(dfn2.head(20))
#     dfn[:20].plot(x="证券简称",y="incr",kind="bar",rot="30")
#     dfn2[:20].plot(x="证券简称",y="incr",kind="bar",rot="30")
    
    return dfn[:20],dfn2[:20]
    
    
def convert_number(a):
    return int(a.replace(",",""))
    
def filter_szse():
    pre_day_str=str(pre_day)
    df1=lreader.read_detail_szse(pre_day_str)
    
    pre2_day_str=str(pre2_day)
    df2=lreader.read_detail_szse(pre2_day_str)
    
    
    df=df1[["证券简称"]]
    df[pre_day_str]=df1["融资余额(元)"].map(convert_number)
    df[pre2_day_str]=df2["融资余额(元)"].map(convert_number)
    df["融资买入额(元)"]=df1["融资买入额(元)"].map(convert_number)
    df=df.filter(like="00", axis=0)
    df["incr"]=df[pre_day_str]/df[pre2_day_str]-1
    df["quant"]=df[pre_day_str]-df[pre2_day_str]
    
    dfn=df.sort_values(by=['incr'],ascending=False)
#     dfn[:20].plot(x="证券简称",y="incr",kind="bar",rot="30")
    print(dfn.head(20))
    
    dfn2=df.sort_values(by=['quant'],ascending=False)
#     dfn2[:20].plot(x="证券简称",y="incr",kind="bar",rot="30")
    print(dfn2.head(20))
    
    return dfn[:20],dfn2[:20]

def process():
    sse1, sse2=filter_sse()
    szse1, szse2=filter_szse()
    
    incr=pd.concat([sse1,szse1])
    ratio = pd.concat([sse2,szse2])
    
    figure,ax=plt.subplots(2,1)
    figure.suptitle(pre_day)
    # ax1=plt.figure(2,1,1)
    incr=incr.sort_values(by=['incr'],ascending=False)
    incr[:20].plot(x="证券简称",y="incr",kind="bar",rot="30",ax=ax[0])
    # ax2=plt.figure(2,1,2)
    ratio=ratio.sort_values(by=["融资买入额(元)"],ascending=False)
    ratio[:20].plot(x="证券简称",y=["quant","融资买入额(元)"],kind="bar",rot="30",ax=ax[1])
    
    
    plt.show()
    
process()