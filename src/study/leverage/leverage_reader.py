# -*- coding: utf-8 -*-

import pandas as pd
import os
from study.leverage import downloader

def read_detail_sse(date_str):
    fpath=os.path.join("sse","rzrqjygk"+date_str+".xls")
    
    if not os.path.exists(fpath):
        print("downloading file for",date_str)
        downloader.download_leverage_sse(date_str)
    
    df=pd.read_excel(fpath,sheet_name="明细信息")
    df["标的证券代码"]=df["标的证券代码"].map(lambda x:str(x) +".SH")
    df.set_index("标的证券代码",inplace=True)
    
    return df

#
def read_detail_szse(date_str):
    fpath=os.path.join("szse","rzrqjygk"+date_str+".xls")
    
    if not os.path.exists(fpath):
        print("downloading file for",date_str)
        downloader.download_leverage_szse(date_str)
    
    df=pd.read_excel(fpath,dtype={'证券代码' :str})
    df["证券代码"]=df["证券代码"].map(lambda x:str(x) +".SZ")
    df.set_index("证券代码",inplace=True)
    
    return df

def read_detail(date_str,exchange):
    if exchange=="sse":
        return read_detail_sse(date_str)
    else:
        return read_detail_szse(date_str)
    
# df=read_detail_szse("2021-06-28")
# print(df)