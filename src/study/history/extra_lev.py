# -*- coding: utf-8 -*-

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import statsmodels.api as sm
from functools import reduce


def model(features,names,prefix):
    split_date="2020-12-31"
    features=features.dropna()
    
    df,test_df=features[:split_date],features[split_date:]
    
    plt.figure(figsize=(11,8))
    
    
    X=df[names]
    X=sm.add_constant(X)
    y=df["close"]
    mod=sm.OLS(y,X).fit()
    print(mod.summary())
        
    plt.subplot(221) 
    ax=mod.resid.plot(label="resid")
    mod.fittedvalues.plot(ax=ax,label="fitted")
    y.plot(ax=ax)
    plt.title("Fit")
    plt.legend()
    mse=np.mean(mod.resid**2)
    print("MSE",mse)
    
    
    z, p = stats.normaltest(mod.resid.values)
    print("p-value",p)
    
    plt.subplot(222)
    plt.hist(mod.resid.values,100)
    plt.title("Resid,p={:.4f}".format(p))
    
    plt.subplot(223)
    plt.plot(df[names[0]],y,'o', label='data')
    plt.plot(df[names[0]],mod.fittedvalues, 'r--.',label='OLS')
    plt.title("Reg")
    plt.legend()
    
    X=test_df[names]
    X=sm.add_constant(X)
    preds=mod.get_prediction(X).summary_frame()
    print(preds.head()[0:1].to_json())
    pred_y=preds["mean"]
    
    
    plt.legend()
    
    ax4=plt.subplot(224)
    test_df["close"].plot(ax=ax4,label="observation")
    pred_y.plot(ax=ax4,label="prediction")
    plt.fill_between(preds.index,preds["obs_ci_lower"],preds["obs_ci_upper"],alpha=0.2)
    last_diff=test_df["close"][-1]-pred_y[-1]
    plt.title("Verify,mse:{:.2f},last diff:{:.2f}".format(mse,last_diff))
    plt.legend()
     
    title=prefix+":"+",".join(names)
    plt.suptitle(title)
    fpath=os.path.join("img",prefix+"_"+"_".join(names)+".png")
    print(fpath)
    plt.savefig(fpath)
    plt.close()



start="2019-12-31"


def get_features(name):
    
    base_dir=name

    price_df=pd.read_csv(os.path.join(base_dir,name+".csv"),encoding="utf8",parse_dates=[0],index_col=0).sort_index()[start:]
    lev_df=pd.read_excel(os.path.join(base_dir,"融资融券_"+name+"n.xls"),parse_dates=[0],index_col=0).sort_index()[start:]
    
    files=os.listdir(name)
    etfs=filter(lambda f: len(f)==10 and f[-3:]=="xls", files)

    
    extra_dfs=map(lambda etfile:pd.read_excel(os.path.join(base_dir,etfile),header=0,parse_dates=[0],index_col=0).sort_index()[start:][["融资余额(元)","融券余量"]],etfs)
    extra_dfs=list(extra_dfs)
        
    extra=reduce(lambda a,b:a+b, extra_dfs)/100000000
    features=price_df[["收盘价"]]

    features=features.rename(columns={"收盘价": "close"})
    features["lev"] =lev_df["融资余额(亿元)"]
    features["sell"]=lev_df["融券余额(亿元)"]
    features["extra_lev"] = extra["融资余额(元)"]
    features["extra_sell"] = extra["融券余量"]
    features["total_lev"]=features["lev"]+features["extra_lev"]
    features["total_sell"]=features["sell"]+features["extra_sell"]

    print(features[-1:])
    
    return features


    
if __name__=="__main__":
    
    for name in ["000905"]:
        features=get_features(name)
#         model(features,["lev"],name)
        model(features,["lev","extra_lev","sell","extra_sell"],name+"t")
#         model(features,["lev","sell"],name)
#         model(features,["total_lev","total_sell"],name)


