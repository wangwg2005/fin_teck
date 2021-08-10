# -*- coding: utf-8 -*-
import datetime
from study.leverage import time_util as tutil
from study.leverage import leverage_reader as lreader
import pandas as pd
import matplotlib.pyplot as plt 
from pandas_datareader import data, wb
import business_day as bd
import yfinance as yf
import json
import file_cache as fc
import os
import numpy as np

ttoday=datetime.date.today()

pre_day=tutil.get_prevous_trade_date(ttoday)

pre2_day=tutil.get_prevous_trade_date(pre_day)

ind=1
dump_path="top"+ind+".json"

def filter_sse():

    pre_day_str=tutil.stringfy(pre_day)
    df1=lreader.read_detail_sse(pre_day_str)
    
    pre2_day_str=tutil.stringfy(pre2_day)
    df2=lreader.read_detail_sse(pre2_day_str)
    
    
    df=df1[["标的证券简称"]]
    df=df.rename(columns={"标的证券简称":"证券简称"})
    df[pre_day_str]=df1["本日融资余额(元)"]
    df[pre2_day_str]=df2["本日融资余额(元)"]
    
    df=df.filter(regex="^60", axis=0)
    df["incr"]=df[pre_day_str]/df[pre2_day_str]-1
    df["quant"]=df[pre_day_str]-df[pre2_day_str]
    
    dfn=df.sort_values(by=['incr'],ascending=False)
    
#     print(dfn.head(20))
    
    dfn2=df.sort_values(by=['quant'],ascending=False)
    
#     print(dfn2.head(20))
#     dfn[:20].plot(x="证券简称",y="incr",kind="bar",rot="30")
#     dfn2[:20].plot(x="证券简称",y="incr",kind="bar",rot="30")
    
    return dfn[:20],dfn2[:20]
    
    
def convert_number(a):
    return int(a.replace(",",""))
    
def filter_szse():
    pre_day_str=str(pre_day)[:10]
    df1=lreader.read_detail_szse(pre_day_str)
    
    pre2_day_str=str(pre2_day)[:10]
    df2=lreader.read_detail_szse(pre2_day_str)
    
    cname1=tutil.stringfy(pre_day)
    cname2=tutil.stringfy(pre2_day)
    
    df=df1[["证券简称"]]
    df[cname1]=df1["融资余额(元)"].map(convert_number)
    df[cname2]=df2["融资余额(元)"].map(convert_number)
    df=df.filter(like="00", axis=0)
    df["incr"]=df[cname1]/df[cname2]-1
    df["quant"]=df[cname1]-df[cname2]
    
    dfn=df.sort_values(by=['incr'],ascending=False)
#     dfn[:20].plot(x="证券简称",y="incr",kind="bar",rot="30")
#     print(dfn.head(20))
    
    dfn2=df.sort_values(by=['quant'],ascending=False)
#     dfn2[:20].plot(x="证券简称",y="incr",kind="bar",rot="30")
#     print(dfn2.head(20))
    
    return dfn[:20],dfn2[:20]

def process():
    sse1, sse2=filter_sse()
    szse1, szse2=filter_szse()
    
    incr=pd.concat([sse1,szse1])
    abs_val = pd.concat([sse2,szse2])
    
    figure,ax=plt.subplots(2,1)
    figure.suptitle(pre_day)
    # ax1=plt.figure(2,1,1)
    incr=incr.sort_values(by=['incr'],ascending=False)
    incr[:20].plot(x="证券简称",y="incr",kind="bar",rot="30",ax=ax[0])
#     incr[:20].plot(y="incr",kind="bar",rot="30",ax=ax[0])
    # ax2=plt.figure(2,1,2)
    ratio=abs_val.sort_values(by=['quant'],ascending=False)
    ratio[:20].plot(x="证券简称",y="quant",kind="bar",rot="30",ax=ax[1],stacked=True)
#     ratio[:20].plot(y="quant",kind="bar",rot="30",ax=ax[1],stacked=True)
    
    
    plt.show()


def dump():
    if os.path.exists(dump_path):
        return
    else:
        print("dummping price data")
    bds=bd.get_business_day_cn("2020")
    days=pd.date_range(start="2020-01-01",end="2020-12-31",freq=bds)
    kv={}
    ind=1
    range_s=ind
    range_e=ind+1
    for i in range(1,len(days)):
        global pre_day, pre2_day
        pre_day=days[i]
        pre2_day=days[i-1]
        sse1, sse2=filter_sse()
        szse1, szse2=filter_szse()
         
        sid=sse2.index[ind] if sse2[range_s:range_e]["quant"].values[0]>szse2[range_s:range_e]["quant"].values[0] else szse2.index[ind]
        print(days[i],sid)
        kv[str(pre_day)[:10]]=sid
        
    #         ratio = pd.concat([sse2,szse2])
    with open(dump_path,"w",encoding="gbk") as ff:
        ff.write(json.dumps(kv))    
    
def batch_analyze():
    dump()
    bds=bd.get_business_day_cn("2020")
#     days=pd.date_range(start="2020-01-01",end="2020-12-31",freq=bds)
    kv={}

    with open(dump_path,"r") as f:
        kv=json.load(f)
    kv2={}
    for k in list(kv.keys())[:-7]:
        sid=kv[k]
        fpath=os.path.join("cache",sid[:6]+".csv")
        
        if os.path.exists(fpath):
            df=pd.read_csv(fpath,index_col="Date",parse_dates=True)
        else:
            print("downloading",sid)
            df=yf.download(sid,start="2020-01-01",end="2020-12-31")
            if len(df)==0:
                print("no data fetched, stopping")
                break
            df.to_csv(fpath)
        term=pd.date_range(start=k,periods=7,freq=bds)
        start_d=term[1]
        cprice=df.at[start_d,"Close"]
        mprice=df[term[2]:term[-1]]["Close"].max()
        rate=mprice/cprice-1
        kv2[k]=rate
        if rate>0.1:
            print(k,sid,rate)
    plt.plot(kv2.keys(),kv2.values())
    ss=list(kv2.values())
    print("mean",np.mean(ss))
    print("median",np.median(ss))
    plt.show()
# process()
batch_analyze()
# dump()