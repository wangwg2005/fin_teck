# -*- coding: utf-8 -*-
import datetime
from study.leverage import time_util as tutil
from study.leverage import leverage_reader as lreader
import pandas as pd
import matplotlib.pyplot as plt
import business_day as bd
import os
import numpy as np
from study.realtime import price_query

import warnings
warnings.simplefilter("ignore")

ttoday=datetime.date.today()

pre_day=tutil.get_prevous_trade_date(ttoday)

pre2_day=tutil.get_prevous_trade_date(pre_day)





def get_price(sid,fname=None):
    print(sid)
    
    if fname is None:
        fname=os.path.join("cache",sid[:6]+".csv")
        
    sid = price_query.convert_sid(sid)
    
    
    if not os.path.exists(fname):
    
        result = price_query.get_history_price(sid)
        print("not exists")
        df=pd.DataFrame(data=result)
        df=df.set_index("day")
        df.to_csv(fname)
    else:
        df = pd.read_csv(fname,index_col="day")
        last_day = df.index[-1]
        days = pd.date_range(start=last_day, end=ttoday,freq=bd.get_business_day_cn("all"))
        
        print(days)
 
        day_num = len(days)
        print("day number",day_num)
        if day_num>3:
            result = price_query.get_history_price(sid)
            print(result[-2:])
            df = pd.DataFrame(data=result)
            df = df.set_index("day")
            diff = df[str(days[1])[:10]:]
            
            new_prices = diff.to_csv(header=False)
            with open(fname,'a', newline='',encoding="utf8") as fo:
                fo.writelines(new_prices)
        
    return df

def bottom_sec_szse():
    last_day="2020-12-31"
    end_date="2021-12-16"
    days=pd.date_range(start = last_day, end= end_date, freq = bd.get_business_day_cn("all"))
    print("days",days)
    days = list(map(lambda day:str(day)[:10], days))
    
    dfs = map(lambda day:lreader.read_detail_szse(day),days)
    
    pre_df=None
    day_it = iter(days)
    
    result = pd.DataFrame()
    
    for df in dfs:
        df=df[~ df["证券简称"].str.contains("ETF")]
        df["融资余额(元)"] = df["融资余额(元)"].apply(lambda a:int(a.replace(",","")))
        
        day = next(day_it)
        if pre_df is None:
            pre_df =  df
            continue
        df["rzye"] = pre_df["融资余额(元)"]
        df["融资净买入"] = df["融资余额(元)"] - df["rzye"]
        row = df.nsmallest(1,"融资净买入")
        t = {"day":day, "证券简称":row.iat[0,0],"证券代码":row.index[0],"融资净买入":row.iat[0,-1]}
#         print(t)
        result = result.append(t,ignore_index=True)
        
        pre_df = df
    
    result.index = pd.to_datetime(result.pop("day"))
    
    return result
    

def update_bottom_secs():
#     buttom = pd.read_csv("buttom.csv")
#     last_day = buttom["day"].max()
    last_day="2021-01-01"
    end_date="2021-12-15"
    days=pd.date_range(start = last_day, end= end_date, freq=bd.get_business_day_cn("all"))
    print("days",days)
    days = list(map(lambda day:str(day)[:10], days))
    sse = map(lambda day : lreader.read_detail_sse(day), days)
#     szse = map(lambda day: lreader.read_detail_szse(day))
    szse = bottom_sec_szse()
    print()
    x=[]
    y=[]
    y1=[]
    y2=[]
    ids=[]
    names=[]
    names1=[]
    names2=[]
    print(szse)
    aa = zip(days,sse)
#     print("size",len(aa))
    for row in aa:
        day =  row[0]
        df = row[1]
        df=df[~ df["标的证券简称"].str.contains("ETF")]
        df["融资净买入"] = df["本日融资买入额(元)"] - df["本日融资偿还额(元)"]
        smallest = df.nsmallest(2,"融资净买入")
        sid = smallest.index[0]
        
        ind=0
        if sid == '600519.SS':
            ind=1
            sid=smallest.index[1]
        
        val_sh = smallest.at[sid,"融资净买入"]
        val_sz = szse.loc[day,"融资净买入"]
        
        if val_sh <=val_sz:
            min_row = smallest.iloc[ind]
        else:
            min_row = szse.loc[day]
            sid = min_row["证券代码"]
        
#         print(min_row)
        name=min_row[0]
        
        
        
#         if "ETF" in name:
#             continue
        ids.append(sid)
        price_df = get_price(sid)[str(day)[:10]:]["close"].map(lambda a:float(a))
#         try:
#         print(price_df)
        time_interval = 10
        if len(price_df) <= time_interval:
            break;
        delta=price_df[time_interval]/price_df[0]-1
#         except:
#             print(price_df)
#             break
        

        

#         if name=="贵州茅台":
#             continue
        
        x.append(day)
        y.append(delta)
        
        if price_df[1]>=price_df[0]:
            y1.append(delta)
            names1.append(name)
        else:
            y2.append(delta)
            names2.append(name)
        names.append(name)

        print(day, name, smallest.index[0], delta)
    
    print(list(zip(x,ids,names)))
    x=pd.to_datetime(x)
    
    plt.plot(x,y)
    print("mean",np.mean(y))
    print("median",np.median(y))
    print("mean1",np.mean(y1))
    print("median1",np.median(y1))
    print("mean2",np.mean(y2))
    print("median2",np.median(y2))
    print(names1)
    print(names2)
    plt.grid()
    plt.show()

        
# update_bottom_secs()
# get_price("000723.sz")
# print(bottom_sec_szse())
# get_price("000002.sz")
