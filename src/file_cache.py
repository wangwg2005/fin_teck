# -*- coding: utf-8 -*-

import os
import pandas as pd
from datetime import datetime, date, timedelta
import calendar

holiday=["2021-01-01"]

tmp_dir=os.path.join(os.getcwd(),"cache")

print("cache dir:",tmp_dir)

cache_only=False
no_cache=False

def skip_holiday(day):
    while str(day) in holiday:
        day=day+timedelta(-1)
        
    return day

def get_prevous_trade_date(currentdate):
    
    
    year= currentdate.year
    month = currentdate.month
    day = currentdate.day
    weekday=calendar.weekday(year,month,day)
    
    result=None
    if weekday==0:
        result=currentdate+timedelta(-3)
    else:
        result=currentdate+timedelta(-1)
        
    result=skip_holiday(result)
            
    return result

def get_from_cache(cache_id):
    if no_cache:
        return pd.DataFrame({"日期":[]})
    fpath=os.path.join(tmp_dir,cache_id+".csv")
    if os.path.exists(fpath):
        df=pd.read_csv(fpath)
        date_time = pd.to_datetime(df.pop('日期'), format='%Y-%m-%d')
        df['日期']=date_time
    else:
        df= pd.DataFrame()
    
    return df

def get_cache(cache_id, func, param=None):
    print("retriving ", cache_id)
    df=get_from_cache(cache_id)
    result=None
    
    if len(df)!=0 and is_up_to_date(df):
        print("retriving %s from cache" %(cache_id))
        result=df
    else:
        print("updating cache for ",cache_id)
        if param is None:
            latest=func()
        else:
            latest=func(param)
        if len(df)>0 and is_up_to_date(latest):
            result=merge(df, latest)
            print("%d new rows got" %(len(result)-len(df)))
        else:
            result=latest
        
    
    
    up_to_date= is_up_to_date(result)
        
    result.index= pd.to_datetime(result.pop('日期'), format='%Y-%m-%d')
    if up_to_date and not no_cache:
        push(cache_id, result)
    return result

def is_up_to_date(df):
    pre_trade_date=get_prevous_trade_date(date.today())
    
    return  len(df.loc[df['日期'] == pre_trade_date])
    

def merge(df1,df2):
#     df1.replace('00','0',regex=True,inplace=True)
#     df2.replace('00','0',regex=True,inplace=True)
    result=pd.concat([df1, df2], axis=0)
    print("size before redundance",len(df1))
    redundance= result.drop_duplicates(subset=["日期"])
    print("size after redundance",len(redundance))
    return redundance


def push(cache_id,pd):
    fpath=os.path.join(tmp_dir,cache_id+".csv")
    pd.to_csv(fpath)
    
    
print("previous trade date",get_prevous_trade_date(date.today()))