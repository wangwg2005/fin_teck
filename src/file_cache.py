# -*- coding: utf-8 -*-

import os
import pandas as pd
from datetime import datetime, date, timedelta
import calendar
import json

holiday=["2021-02-11","2021-02-12","2021-02-13","2021-02-14","2021-02-15","2021-02-16","2021-02-17","2021-04-05"]

# tmp_dir=os.path.join(os.getcwd(), "cache")
tmp_dir=r"C:\Users\Darren\eclipse-workspace\fin_study\src\study\cache"

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

ptd=get_prevous_trade_date(date.today())

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

def convert_index_to_date(df, iname="日期"):
    df.index = pd.to_datetime(df.pop(iname), format='%Y-%m-%d')


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
        u2d=is_up_to_date(latest)
        print("is up to date:",u2d)
        if len(df)>0 and u2d:
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
    return  len(df[df['日期'] == str(ptd)])
    

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
    
    
def json_cache(fname,get_func,*param):
    fpath=os.path.join(tmp_dir,fname)
    if os.path.exists(fpath):
        with open(fpath,"r",encoding="utf8") as f:
            j= json.load(f)
            return j
    else:
        result= get_func(*param)
        print("to cache",result)
        with open(fpath,"w",encoding="utf8") as f:
            json.dump(result, f)
        print("caching",fpath)
        return result
    
print("previous trade date", ptd)


def test_file(cache_id):
    df=get_from_cache(cache_id)
    df=df.sort_values(by="日期")
    print(df)
    
#test_file("csi500")