# -*- coding: utf-8 -*-

import pandas as pd
import os
from study.leverage import downloader
import sys

abs_dir=None

# def get_current_path():
abs_file=__file__
abs_dir=abs_file[:abs_file.rfind(os.sep)] 
    

def read_detail_sse(date_str):
    dstr=date_str.replace("-","")
    fpath=os.path.join(abs_dir,"sse","rzrqjygk"+dstr+".xls")
    print(fpath)
    if not os.path.exists(fpath):
#         print("downloading file for",date_str)
        downloader.download_leverage_sse(dstr)
    
    df=pd.read_excel(fpath,sheet_name="明细信息")
    df["标的证券代码"]=df["标的证券代码"].map(lambda x:str(x) +".SS")
    df.set_index("标的证券代码",inplace=True)
    
    return df

#
def read_detail_szse(date_str):
    if len(date_str)>10:
        date_str=date_str[:10]
    fpath=os.path.join(abs_dir,"szse","rzrqjygk"+date_str+".xls")
    
    if not os.path.exists(fpath):
        print("downloading file for",date_str)
        downloader.download_leverage_szse(date_str)
#     else:
#         print("file exists, skip downloading, date:",date_str)
    
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