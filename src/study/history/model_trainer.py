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

historys=["000016","000300"]
his_dfs=[read_history(his) for his in historys ]

leves=["上证50","沪深300"]
leve_dfs=[read_leverage(leve) for leve in leves]

# train sse50

feature_sse50=his_dfs[0][["收盘价"]][:trade_days]
feature_sse50["lev"]=leve_dfs[0]["融资余额(亿元)"]

feature_sse50=feature_sse50.dropna()

train_level=3

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





