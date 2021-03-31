# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import model_util as mu
import os

from sklearn.linear_model import LinearRegression
from importlib_metadata import files

trade_days=1000

def read_history(fname):
    df=pd.read_csv(fname,encoding="gbk",parse_dates=[0],index_col=0)
    return df

def read_leverage(fname):
    df = pd.read_excel(fname,header=1, encoding="gbk",parse_dates=[0],index_col=0)
    return df

def get_sub_set(df,start_date, end_date):
    return df[end_date:start_date]

### price file first , leverage data second
def read_dir(path):
    files = os.listdir( path );
    
    if files[0][-3:]=="csv":
        return files
    else :
        return (files[1],files[0])
    

def model1_train(root,train_start="2019-01-01", train_end="2020-12-31", his_start="2015-01-01", his_end=""):
    
#     features=csi500[["最高价","最低价","开盘价","收盘价"]]
#     print(features)
#     root="csi500"
    price_file, leverage_file=read_dir(root)
    
    csi500=read_history(os.path.join(root,price_file))
    f1=os.path.join(root,leverage_file)
    print(f1)
    leve_csi500=read_leverage(f1)
    
    features=csi500[["收盘价","成交量"]]
    print(csi500.index.duplicated())
    features["lev"]=leve_csi500["融资余额(亿元)"]
    features.dropna(inplace=True)
    
    train_date=("2019-01-01","2020-12-31")
    train_set=get_sub_set(features, *train_date)
#     print(train_set)
    
    lr=LinearRegression()
#     X=np.array(train_set["lev"]).reshape(1, -1)
#     y=np.array(train_set["收盘价"]).reshape(1, -1)
    lr.fit(train_set[["lev"]], train_set["收盘价"])
    
    features["pred"]=lr.predict(features[["lev"]])
    features["resid"]=features["收盘价"]-features["pred"]
    features["resid_norm"]=features["resid"]/features["收盘价"]
#     features[:"2020-01-01"].plot(grid=True)
#     plt.show()
    features['成交量'] = features['成交量'].astype('float64')
    features[:his_start][["收盘价","resid","resid_norm"]].plot(grid=True,subplots=True,title=root)
    
    
#     test_set["pred"]=lr.predict(np.array(test_set["lev"]).reshape(1, -1))
    
    
#     test_set.plot(grid=True)
names=["csi500","hs300","399006","000016"]
for name in names:
    model1_train(name)
plt.show()