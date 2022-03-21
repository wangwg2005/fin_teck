# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import model_util as mu


trade_days=1000

def read_history(fname):
    df=pd.read_csv(fname+".csv",encoding="gbk")
    date_time = pd.to_datetime(df.pop('日期'), format='%Y-%m-%d')
    df.index=date_time
    return df

def read_leverage(fname):
    df = pd.read_excel("融资融券"+fname+".xls",header=1, encoding="gbk")
    date_time = pd.to_datetime(df.pop('交易日期'), format='%Y-%m-%d')
    df.index=date_time
    return df


def index_trainer():
    historys=["000016","000300"]
    his_dfs=[read_history(his) for his in historys ]
    
    leves=["上证50","沪深300"]
    leve_dfs=[read_leverage(leve) for leve in leves]
    
    # train sse50
    
    feature_sse50=his_dfs[0][["收盘价"]][:trade_days]
    feature_sse50["lev"]=leve_dfs[0]["融资余额(亿元)"]
    
    feature_sse50=feature_sse50.dropna()
    
    train_level=1
    
    m_sse50=mu.train_model(feature_sse50["lev"],feature_sse50["收盘价"],level=train_level)
    
    feature_sse50["sim"]=m_sse50[1]
    feature_sse50.plot()
    plt.show()
    
    #train csi300
    csi300=his_dfs[1][["收盘价"]][:trade_days]
    csi300["lev"]=leve_dfs[1]["融资余额(亿元)"]
    
    csi300=csi300.dropna()
    m_csi300=mu.train_model(csi300["lev"],csi300["收盘价"],level=train_level)
    csi300["sim"]=m_csi300[1]
    csi300.plot()
    plt.show()


def multiple_factor_trainer():
    df=read_history("000905")
    features=df[["最高价","最低价","开盘价","收盘价"]]
#     print(features)
    
    leve_csi500=read_leverage("中证500")
#     print(leve_csi500)
    features["lever"]=leve_csi500["融资余额(亿元)"]
    
    
    features=features[features["最高价"]<8000]
    features=features.dropna()
#     features=features[:1000]
    
    m1 = mu.train_model(np.array(features["lever"].tolist()),np.array(features["最高价"].tolist()))
    m2 = mu.train_model(np.array(features["lever"].tolist()),np.array(features["最低价"].tolist()))
    m3 = mu.train_model(np.array(features["lever"].tolist()),np.array(features["开盘价"].tolist()))
    m4 = mu.train_model(np.array(features["lever"].tolist()),np.array(features["收盘价"].tolist()))
    features["sim_high"]=m1[1]
    features["sim_low"]=m2[1]
    features["sim_open"]=m3[1]
    features["sim_close"]=m4[1]
    
    
    pd.set_option('display.width', 200)
    pd.set_option('max_columns', 100)
    print(features)
    f_high=features[["最高价"]]
    f_high["sim_high"]=m1[1]
#     f_high.plot(grid=True)
    
    f_low=features[["最低价"]]
    f_low["sim_low"]=m2[1]
#     f_low.plot(grid=True)
    
    f_open=features[["开盘价"]]
    f_open["sim_open"]=m3[1]
#     f_open.plot(grid=True)
    f_sim=features[["sim_close","收盘价"]]
    f_sim.plot(grid=True)
    
    plt.show()


# multiple_factor_trainer()

def train(name):
    his = read_history(name)
    lev = read_leverage(name)