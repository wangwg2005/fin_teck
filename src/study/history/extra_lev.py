# -*- coding: utf-8 -*-

import pandas as pd
import os
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.api as sm
from functools import reduce
from sklearn.linear_model import RidgeCV,Ridge
import numpy as np

# data_size=[20,1]

start="2017-12-31"

def model(features,names,prefix):
    split_date="2020-12-31"
#     print(features[-10:])
    features=features[[*names,"close"]]
    features = features.dropna()
    print('last trade day',features.index[-1])
    df,test_df=features[:split_date],features[split_date:]
#     df=df[-data_size[0]:]

    print('df',df.tail())
    
    print('test',test_df.tail())
    
    plt.figure(figsize=(11,8))
    
#     for name in names:
#         df[name+'_square']=df[name]**2
    
    X=df[names]
#     rx=X.to_numpy()
    X=sm.add_constant(X)
    y=df["close"]
    
    print('x',X)
    print('y',y)
    mod=sm.OLS(y,X).fit()
    print(mod.summary())
    
    

#     
#      
#     alphas=[i/10 for i in range(1,400)]
#       
#     coefs = []
#     for a in alphas:
#         ridge = Ridge(alpha=a)
#         ridge.fit(X, y)
#         coefs.append(ridge.coef_)
#       
#     
#     
#     rm = RidgeCV(alphas=[i/10 for i in range(1,400)])
#     rm.fit(rx, y.to_numpy())
        
    plt.subplot(221) 
#     ax=mod.resid.plot(label="resid")
    ax = mod.fittedvalues.plot(label="fitted")
    y.plot(ax=ax)
    plt.title("Fit")
    plt.legend()
    print("MSE",mod.mse_total)
    
    
    z, p = stats.normaltest(mod.resid.values)
#     p =  mod.f_pvalue
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
#     rX= X.to_numpy()
    X=sm.add_constant(X)
    preds=mod.get_prediction(X).summary_frame()
    print(X.index[-1])
    print(test_df["close"][-1])
    
    
    
#     y_rpred = rm.predict(rX)
    print(preds)
    
    
    pred_y=preds["mean"]
    
    
    plt.legend()

    fpath = os.path.join("img", prefix + "_" + "_".join(names) + ".png")
    plt.savefig(fpath)
    plt.close()

    plt.figure(figsize=(11, 8))
    plt.grid()
    ax4=plt.subplot(211)
#     print("ridge",y_rpred)
#     preds["Ridge"]=y_rpred   57618539
    test_df["close"].plot(ax=ax4,label="observation")
#     preds["Ridge"].plot(ax=ax4, label='Ridge')
    
    print(preds[["mean","obs_ci_lower","obs_ci_upper"]][-5:])
    
    pred_y.plot(ax=ax4,label="prediction")
    plt.fill_between(preds.index,preds["obs_ci_lower"],preds["obs_ci_upper"],alpha=0.2)
    last_diff=test_df["close"][-1]-pred_y[-1]
    plt.title("{},mse:{:.2f},last diff:{:.2f}".format(test_df.index[-1].strftime("%Y%m%d"),mod.mse_total,last_diff))
    plt.legend()

    ax5 = plt.subplot(212)
    residual=pred_y-test_df["close"]
    residual.plot(ax=ax5,label="residual")
    plt.legend()

    title=prefix+":"+",".join(names)
    plt.suptitle("predtion")
    fpath = os.path.join("img", prefix + "_" + "_".join(names) + "_pred.png")
    plt.savefig(fpath)
    print(fpath)

    plt.close()






def get_features(name):
    
    base_dir=name

    price_df=pd.read_csv(os.path.join(base_dir,name+".csv"),encoding="utf8",parse_dates=[0],index_col=0,nrows=4000).sort_index()[start:]
    lev_df=pd.read_excel(os.path.join(base_dir,"融资融券_"+name+"n.xls"),parse_dates=[0],index_col=0).sort_index()[start:]
    
    files=os.listdir(name)
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

def square_process(df,names):
    for name in names:
        df[name+"_square"]=df[name]**2
         
    
    return df
    
if __name__=="__main__":
    
    for name in ["000905"]:
        features=get_features(name)
#         model(features,["lev","f1"],name)
#         print(features[-1:])
#         model(features,["lev","extra_lev","sell","extra_sell","f1"],name)
#         model(features,["lev","extra_lev","sell","extra_sell"],name)

        model(features,["lev","sell"],name)

#         features['lev_square']=features['lev']**2
#         features['sell_square']=features['sell']**2
#         model(features,["lev","sell","lev_square","sell_square"],name)
#         model(features,["total_lev","total_sell"],name)
#         model(features,["total_lev","total_sell","f1"],name)


