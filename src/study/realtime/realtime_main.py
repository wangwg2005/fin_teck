# -*- coding: utf-8 -*-

import pandas as pd
import datetime
import yfinance as yf
from study.realtime import boll
from study.realtime import price_query
import time
import json
import business_day as bd
import numpy as np
import study.leverage.main2 as m2
import os
    
#     time.sleep(3)
today_str=str(datetime.date.today()) 

def load_model():
    with open("model1_mean_30.json","r") as f:
        model= json.load(f)
        return model
    
def load_stocks(duration):
    
    
    days=pd.date_range(end=today_str, periods=duration+1, freq=bd.get_business_day_cn("2021"))

    sid=[]
    
    for day in days[:duration]:
        fpath="..\\cache\\"+day+"_incr.csv"
        with open(fpath,'r') as f:
            f.read_line()
            l=f.read_line()
            sid=l[:9]
            
    return sid.reverse()

def sell(sid,curr_price,target_price):
    print(sid,"should be sold out, target price:",target_price,"current price",curr_price,",",curr_price/target_price-1)

def buy(sid,curr_price,target_price):
    print(sid,"should be bought in, target price:",target_price,"current price",curr_price,",",curr_price/target_price-1)

def monitor(sids,val):
    
    while True:
        res=price_query.get_price(*sids)
        curr=list(map(lambda r:float(r["current"]),res))
        for j in range(len(sids)):
            if curr[j]>val[j][0]:
                sell(sids[j],curr[j],val[j][0])
            elif curr[j]<val[j][1]:
                buy(sids[j],curr[j],val[j][1])
        print("sleep 3 seconds--------------")
        time.sleep(3)
                
def prepare_leverage_data(duration):
    year="2021"
    bds=bd.get_business_day_cn(year)
    print(today_str)
    days=pd.date_range(end=today_str,periods=duration+2,freq=bds)
    
    vals=[]
    
    for i in range(1,duration+1):
        m2.pre_day=str(days[i])[:10]
        m2.pre2_day=str(days[i-1])[:10]
        fname="..//cache//top_sec_"+m2.pre_day+".json"
        if os.path.exists(fname):
            with open(fname,'r',encoding="gbk") as ff:
                vals.append(json.load(ff))
        else:
            sse1, sse2, sse3, sse4=m2.filter_sse()
            szse1, szse2,szse3,szse4=m2.filter_szse()
            
            top_quant=m2.merge_ordered(sse1, szse1, "quant")[:10]
            top_ratio=m2.merge_ordered(sse2, szse2, "incr")[:10]
            buttom_quant=m2.merge_ordered(sse3, szse3, "quant",ascending=True)[:10]
            buttom_ratio=m2.merge_ordered(sse4, szse4, "incr",ascending=True)[:10]
             
            val={"quant_top":top_quant.index.to_list(),"quant_buttom":buttom_quant.index.to_list(),"ratio_top":top_ratio.index.to_list(),"ratio_buttom":buttom_ratio.index.to_list()}
#             print(days[i],val)
    #         kv[str(pre_day)[:10]]=val
            vals.append(val)
            with open(fname,"w",encoding="gbk") as ff:
                ff.write(json.dumps(val))
                
    return vals

def prepare_prices(sids):
    prices=[]
    
    size=len(sids)
    for i in range(size):
        p=price_query.get_history_price(sids[i], size-i)
        print(p)
    
        prices.append(p[0])
        
    print(prices)
    return np.array(prices)
    
    
if __name__ == '__main__':
    
    model=load_model()['quant_buttom']
    duration=len(model["high"])
    datas=prepare_leverage_data(duration)
    
    sids=list(map(lambda a:price_query.convert_sid(a["quant_buttom"][0]),datas))
    prices=prepare_prices(sids)
    print(prices)
    base_prices=np.array(list(map(lambda a:float(a["close"]),prices)))

    monitor_val=zip((np.array(model["high"])+1)*base_prices,(1+np.array(model["low"]))*base_prices)
    monitor(sids,list(monitor_val))
        
        
    
    
# print(df)
