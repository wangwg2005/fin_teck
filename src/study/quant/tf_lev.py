# -*- coding: utf-8 -*-
import tensorflow as tf

import os
from functools import reduce
import numpy as np
import pandas as pd


start="2020-10-31"


def get_features(name):
    
    base_dir=os.path.join("..","history",name)

    price_df=pd.read_csv(os.path.join(base_dir,name+".csv"),encoding="utf8",parse_dates=[0],index_col=0,nrows=4000).sort_index()[start:]
    lev_df=pd.read_excel(os.path.join(base_dir,"融资融券_"+name+"n.xls"),parse_dates=[0],index_col=0).sort_index()[start:]
    
    files=os.listdir(base_dir)
    etfs=filter(lambda f: len(f)==15 and f[:4]=="rzrq", files)

    
    extra_dfs=map(lambda etfile:pd.read_csv(os.path.join(base_dir,etfile),header=0,parse_dates=[0],index_col=0).sort_index()[start:][["融资余额(元)","融券余量"]],etfs)
    extra_dfs=list(extra_dfs)
#     for ext in extra_dfs:
#         print(ext.dtypes)
# #         print(ext)
#         print(ext.head())
#         print(ext.index[:10])
        
    extra=reduce(lambda a,b:a+b, extra_dfs)/100000000
    features=price_df[["收盘价"]]
    features["f1"]=price_df["成交量"]*price_df["涨跌幅"].map(lambda a: 1 if a>0 else -1)/10000000
    features=features.rename(columns={"收盘价": "close"})
    features["lev"] =lev_df["融资余额(亿元)"]
    features["sell"]=lev_df["融券余量(亿股)"]
    features["extra_lev"] = extra["融资余额(元)"]
    features["extra_sell"] = extra["融券余量"]
    features["total_lev"]=features["lev"]+features["extra_lev"]
    features["total_sell"]=features["sell"]+features["extra_sell"]
    
    return features


def train():
    pass


if __name__ == "__main__":
    print(get_features("000905"))