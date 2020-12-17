# -*- coding: utf-8 -*-

import os
import pandas as pd
from datetime import datetime, date, timedelta

tmp_dir="C:\\tmp\\cache"

def get_from_cache(cache_id):
    fpath=os.path.join(tmp_dir,cache_id+".csv")
    if os.path.exists(fpath):
        df=pd.read_csv(fpath)
        date_time = pd.to_datetime(df.pop('日期'), format='%Y-%m-%d')
        df.index=date_time
    else:
        df= pd.DataFrame()
    
    return df

def get_cache(cache_id, func, param=None):
    print("retriving ", cache_id)
    df=get_from_cache(cache_id)
    result=None
    if is_up_to_date(df):
        print("retriving %s from cache" %(cache_id))
        result=df
    else:
        print("updating cache for ",cache_id)
        if param is None:
            latest=func()
        else:
            latest=func(param)
        if len(df)>0:
            result=merge(df, latest)
        else:
            result=latest
        push(cache_id, result)
        
    return result

def is_up_to_date(df):
    today=date.today()+timedelta(-1)
    return today in df.index
    

def merge(df1,df2):
     return pd.concat([df1, df2], axis=0)


def push(cache_id,pd):
    fpath=os.path.join(tmp_dir,cache_id+".csv")
    pd.to_csv(fpath)
    
        

