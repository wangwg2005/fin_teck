# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import model_util as mu

from sklearn.linear_model import LinearRegression

trade_days=1000

def read_history(fname):
    df=pd.read_csv(fname+"_latest.csv",encoding="gbk",parse_dates=[0],index_col=0)
    return df

def read_leverage(fname):
    df = pd.read_excel("融资融券"+fname+"_all_latest.xls",header=1, encoding="gbk",parse_dates=[0],index_col=0)
    return df

def get_sub_set(df,start_date, end_date):
    return df[end_date:start_date]
    

def model1_train():
    csi500=read_history("000905")
#     features=csi500[["最高价","最低价","开盘价","收盘价"]]
#     print(features)
    
    leve_csi500=read_leverage("中证500")
    
    features=csi500[["收盘价"]]
    features["lev"]=leve_csi500["融资余额(亿元)"]
    features.dropna(inplace=True)
    
    train_date=("2020-01-01","2020-12-31")
    train_set=get_sub_set(features, *train_date)
#     print(train_set)
    
    test_date=("2021-01-01","2021-03-15")
    test_set=get_sub_set(features, *test_date)
    
    lr=LinearRegression()
#     X=np.array(train_set["lev"]).reshape(1, -1)
#     y=np.array(train_set["收盘价"]).reshape(1, -1)
    lr.fit(train_set[["lev"]], train_set["收盘价"])
    
    print(train_set["lev"].shape)
    pred=lr.predict(train_set[["lev"]])
    print(features.shape)
    print(len(pred))
    print(pred)
#     train_set["pred"]=pred
#     train_set["resid"]=train_set["收盘价"]-train_set["pred"]+4000
    
#     train_set.plot(grid=True)
#     plt.show()
    
    features["pred"]=lr.predict(features[["lev"]])
    features["resid"]=features["收盘价"]-features["pred"]
    features["resid_norm"]=features["resid"]/features["收盘价"]
    features[:"2020-01-01"].plot(grid=True)
    plt.show()
    features[:"2020-01-01"][["resid","resid_norm"]].plot(grid=True,subplots=True)
    
    plt.show()
#     test_set["pred"]=lr.predict(np.array(test_set["lev"]).reshape(1, -1))
    
    
#     test_set.plot(grid=True)

model1_train()