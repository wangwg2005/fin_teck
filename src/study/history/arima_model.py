# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import pandas as pd
from study.history import model_trainer2 as mt
import os
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
import numpy as np
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf
import statsmodels
import business_day as bd


def get_df(name):
    files=list(map(lambda a:os.path.join(name,a),mt.read_dir(name)))
    
    sli=slice("2020-07-31","2020-07-31")
    
    prices=mt.read_history(files[0])[sli]
    
    lever=mt.read_leverage(files[1])[sli]
    
    df=prices[["收盘价"]]
    df["lev"]=lever["融资余额(亿元)"]
    df=df.rename(columns={"收盘价":"price"})
    df=df.dropna()
    df=df.sort_index()
    return df

def analyze(name):
    df=get_df(name)
    tsv=df["price"].diff(1)[1:].to_numpy()
    dftest = adfuller(tsv,autolag='AIC')
    print(dftest)
    
def autocorrelation(timeseries, lags):
    fig = plt.figure(figsize=(12, 8))
    ax1 = fig.add_subplot(211)
    plot_acf(timeseries, lags=lags, ax=ax1)
    ax2 = fig.add_subplot(212)
    plot_pacf(timeseries, lags=lags, ax=ax2)
    plt.show()
    
def detect(name,lag):
    df=get_df(name)
    autocorrelation(df["price"].diff(1).dropna(), lag)
    
def diff(timeseries):
    timeseries_diff1 = timeseries.diff(1)
    timeseries_diff2 = timeseries_diff1.diff(1)

    timeseries_diff1 = timeseries_diff1.fillna(0)
    timeseries_diff2 = timeseries_diff2.fillna(0)

    timeseries_adf = adfuller(timeseries['value'].tolist())
    timeseries_diff1_adf = adfuller(timeseries_diff1['value'].tolist())
    timeseries_diff2_adf = adfuller(timeseries_diff2['value'].tolist())

    print('timeseries_adf : ', timeseries_adf)
    print('timeseries_diff1_adf : ', timeseries_diff1_adf)
    print('timeseries_diff2_adf : ', timeseries_diff2_adf)

    plt.figure(figsize=(12, 8))
    plt.plot(timeseries, label='Original', color='blue')
    plt.plot(timeseries_diff1, label='Diff1', color='red')
    plt.plot(timeseries_diff2, label='Diff2', color='purple')
    plt.legend(loc='best')
    plt.show()
    
def model(name):
    files=list(map(lambda a:os.path.join(name,a),mt.read_dir(name)))
    df=mt.read_leverage(files[1])
    df=df.sort_index()
    df=df.rename(columns={"融资余额(亿元)":"lev"})
    
    ser=df["lev"].diff(1).dropna()
    train_val=ser["2020-01-02":"2020-12-29"]
    m = ARIMA(train_val, order=(1,1,1))
    model_fit=m.fit()
    print(model_fit.summary())
    
#     residuals = pd.DataFrame(model_fit.resid)
#     fig, ax = plt.subplots(1,2)
#     residuals.plot(title="Residuals", ax=ax[0])
#     residuals.plot(kind='kde', title='Density', ax=ax[1])
#     plt.show()
    
#     model_fit.plot_diagnostics(figsize=(15, 12))

    pred=model_fit.get_prediction(start=0,dynamic=True)
    pred_ci=pred.conf_int()
    ax0=train_val.plot(label="observation")
    pred.predicted_mean.plot(ax=ax0,label="predicted",alpha=0.7,color="red")
    ax0.fill_between(pred_ci.index,
            pred_ci.iloc[:, 0],
            pred_ci.iloc[:, 1], color='k', alpha=.25)
    
    

#     leng=30
#     ind=pd.date_range("2021-01-01", periods=leng,freq=bd.get_business_day_cn("2021"))
#      
#     obs=ser[ind[0]:ind[-1]]
#     ax=obs.plot(label="Observed")
#      
# #     ax=ser.plot(label='observed')
#     pred_dynamic=model_fit.forecast(steps=leng,index=ind)
#      
# #     pred_ci = pred_dynamic.conf_int()
#     pred_dynamic.plot(label='Dynamic Forecast',ax=ax)
#      
# #     ax.fill_between(pred_ci.index,
# #                 pred_ci.iloc[:, 0],
# #                 pred_ci.iloc[:, 1], color='k', alpha=.25)
#     ax.set_xlabel('Date')
#     ax.set_ylabel('CO2 Levels')
    
    plt.legend()
    
    
    plt.show()
    
    
if __name__=="__main__":
    names=["000905","000300","399006","000016"]
    
#     detect("000905",20)
    model("000905")
#     analyze("000905")
#     for name in names:
#         print(name)
#         analyze(name)


