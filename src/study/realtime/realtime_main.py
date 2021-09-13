# -*- coding: utf-8 -*-

import pandas as pd
import datetime
import yfinance as yf
from study.realtime import boll
from study.realtime import price_query
import time
# stk1, stk2=main2.process(retn=True)
today_str=str(datetime.date.today())
# today_str='2021-09-09'
fpath="..\\cache\\"+today_str+"_incr.csv"
df1=pd.read_csv(fpath,index_col=0)
print(df1)
sids=df1.index.to_list()
# sids2=list(map(lambda s:s[-2:]+s[:6],sids))
print(df1.columns)
if len(df1.columns)<8:
    
    deviation=[]
    close_price=[]
    mean_val=[]
    
    for sid in sids:
        ticker = yf.Ticker(sid)
        
        hour=int(str(datetime.datetime.now())[11:13])
        
        per='20' if hour<9 else '21'
        
        
        df=ticker.history(period=per+'d')
        
        
        boll_mean,boll_dev=boll.get_boll(df[:20])
    #     print(df)
        last_close=df.iat[19,3]
        mean_val.append(boll_mean)
        close_price.append(last_close)
    #     today_close=df.iat[20,3]
        today_close=df.iat[len(df)-1,3]
        upper_value=boll_mean+boll_dev
        dev=(last_close-boll_mean)/boll_mean
    #     if last_close<=upper_value:
        dev_diff=boll_dev-dev
        deviation.append(boll_dev)
        print(sid,dev_diff,today_close/last_close-1)
        
    df1["deviation"]=deviation
    df1["close"]=close_price
    df1['mean']=mean_val
    df1.to_csv(fpath)
    
# print(df)
sid_sina=list(map(lambda s: s[-2:].replace('SS','SH')+s[ :6] , sids))
for i in range(1024):
    res=price_query.get_price(*sid_sina)
    curr=list(map(lambda r:float(r["current"]),res))
    df1["current"]=curr
    df1["realtime_dev"]=df1['deviation']-(df1['current']/df1['mean']-1)
    print(df1[df1["realtime_dev"]>5][["realtime_dev",'current']])
    print(res[0]['date']+" "+res[0]["time"])
    
    
    
    
    time.sleep(3)
    
    

    
# print(df)
