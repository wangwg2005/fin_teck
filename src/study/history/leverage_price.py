# -*- coding: utf-8 -*-

import pandas as pd
import math
import matplotlib.pyplot as plt
import os
import numpy as np
import model_util as models


def cvt_path(fname):
    return fname
#     return os.path.join("study", "history", fname)

start_date="2013-01-01"

leve_csi500 = pd.read_excel(cvt_path("融资融券中证500.xls"),header=1, encoding="gbk")
pred_csi500 = pd.read_excel(cvt_path("融资融券中证500_all_latest.xls"),header=1, encoding="gbk")
leve_csi300 = pd.read_excel(cvt_path("融资融券沪深300.xls"),header=1, encoding="gbk")
leve_total = pd.read_excel(cvt_path("融资融券全市场.xls"),header=1, encoding="gbk")

price_csi500=pd.read_csv(cvt_path("000905.csv"), encoding="gbk")

 
# len=min(len(leve_csi500),len(leve_total),len(price_csi500))
len=200


def mode_std(b):
    a = b - 800
    return 3000*math.cos(a/60-0.55)+5000+80*math.cos(a/5 *math.pi)

 
features=pd.DataFrame()

date_time = pd.to_datetime(price_csi500.pop('日期'), format='%Y-%m-%d')
price_csi500.index=date_time

date_time = pd.to_datetime(pred_csi500.pop('交易日期'), format='%Y-%m-%d')
pred_csi500.index=date_time
pred_csi500=pred_csi500[:"2020-01-01"]

date_time = pd.to_datetime(leve_csi500.pop('交易日期'), format='%Y-%m-%d')
leve_csi500.index=date_time

date_time = pd.to_datetime(leve_total.pop('日期'), format='%Y-%m-%d')
leve_total.index=date_time

features["price"]=price_csi500["收盘价"]
features["lev500"]=leve_csi500["融资余额(亿元)"]
# features["融资余额"]=leve_total["融资余额(亿元)"]
# features["risk1"]=series1=(features["price"]-1000-features["融资余额500"])*2
# features["risk2"]=series1=(2.7*features["price"]-1000-features["融资余额"])*2
# features["risk3"]=features["price"]/features["融资余额500"]*1000+4000


# features=features[(features.price<8000) & (features.lev500>1000)]
train_data=features[features.price<8000][start_date:]
train_data=features.dropna()[:"2013-01-01"]
# features=features[:400]
# print(features)
# print(np.array(features["融资余额500"].tolist()))
# print(np.array(features["price"].tolist()))
# m = models.train_model(np.array(train_data["lev500"].tolist()),np.array(train_data["price"].tolist()))

# features["predict"]=m[0].predict(features["lev500"])

# features=features[:"2020-01-01"]
def predict_csi500_2020():
     
 
    import model_util
    features["predict"]=model_util.csi500["close"].predict(pred_csi500["融资余额(亿元)"])
      
#     features=features[:"2020-01-01"]
    features.plot(grid=True)
    plt.show()
    
    
def non_liner():
#     pred_df=features[:"2020-01-01"]
    pred_df=features[:"2013-01-01"]
    pred_df["predict"]=models.csi500["close"].predict(pred_df["lev500"]+10)
    pred_df["residual"]=pred_df["price"]-pred_df["predict"]
    print(pred_df["residual"][:"2020-01-01"].mean())
#     features=features[:"2020-01-01"]
    pred_df["residual"][:"2020-01-01"].plot(grid=True)
    plt.show()
     
# predict_csi500_2020()
non_liner()



