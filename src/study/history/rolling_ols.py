# -*- coding: utf-8 -*-

import pandas as pd
import os
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.api as sm
from functools import reduce
from sklearn.linear_model import RidgeCV,Ridge
from statsmodels.regression.rolling import RollingOLS
import numpy as np



def model(features,names,prefix):

    
    features=features.dropna()
    print(features[-10:])
    print('last trade day',features.index[-1])
    result = pd.DataFrame()
    for i in range(6,300):
        
        df,test_df=features[-i:-1],features[-1:]
        
    #     plt.figure(figsize=(11,8))
        
        X=df[names]
        X=sm.add_constant(X)
        y=df["close"]
        
        
        
        
        mod=sm.OLS(y,X).fit()
        
        
        X1=test_df[names]
        X2 = sm.add_constant(X1, has_constant='add')
        
        
        preds=mod.get_prediction(X2).summary_frame()
        pred_y=preds.iloc[-1]
        result = result.append(pred_y,ignore_index=True)
        
        
    pd.set_option("max_columns",10)    
    print(result.head(50))
    result["mean"].plot()
    plt.grid(True)
    plt.axhline(features["close"][-1],c='r',ls='--',lw=2)
    plt.fill_between(result.index,result["mean_ci_lower"],result["mean_ci_upper"],alpha=0.2)
    plt.show()
    
#     rols = RollingOLS(y,X, window=60)
#     rres = rols.fit()
#     params = rres.params.copy()
# #     params.index = np.arange(1, params.shape[0] + 1)
#     print(params.tail())
#     fig = rres.plot_recursive_coefficient(variables=names, figsize=(14, 6))
#     plt.show()
    
#     mod=sm.OLS(y,X).fit()
#     print(mod.summary())
    
    

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
        
#     plt.subplot(221) 
# #     ax=mod.resid.plot(label="resid")
#     ax = mod.fittedvalues.plot(label="fitted")
#     y.plot(ax=ax)
#     plt.title("Fit")
#     plt.legend()
#     print("MSE",mod.mse_total)
#     
#     
#     z, p = stats.normaltest(mod.resid.values)
#     print("p-value",p)
#     
#     plt.subplot(222)
#     plt.hist(mod.resid.values,100)
#     plt.title("Resid,p={:.4f}".format(p))
#     
#     plt.subplot(223)
#     plt.plot(df[names[0]],y,'o', label='data')
#     plt.plot(df[names[0]],mod.fittedvalues, 'r--.',label='OLS')
#     plt.title("Reg")
#     plt.legend()
#     
#     X=test_df[names]
# #     rX= X.to_numpy()
#     X=sm.add_constant(X)
#     preds=mod.get_prediction(X).summary_frame()
#     print(X.index[-1])
#     print(test_df["close"][-1])
#     
#     
#     
# #     y_rpred = rm.predict(rX)
#     print(preds)
#     
#     
#     pred_y=preds["mean"]
#     
#     
#     plt.legend()
# 
#     fpath = os.path.join("img", prefix + "_" + "_".join(names) + ".png")
#     plt.savefig(fpath)
#     plt.close()
# 
#     plt.figure(figsize=(11, 8))
#     plt.grid()
#     ax4=plt.subplot(211)
# #     print("ridge",y_rpred)
# #     preds["Ridge"]=y_rpred   57618539
#     test_df["close"].plot(ax=ax4,label="observation")
# #     preds["Ridge"].plot(ax=ax4, label='Ridge')
#     
#     print(preds[["mean","obs_ci_lower","obs_ci_upper"]][-5:])
#     
#     pred_y.plot(ax=ax4,label="prediction")
#     plt.fill_between(preds.index,preds["obs_ci_lower"],preds["obs_ci_upper"],alpha=0.2)
#     last_diff=test_df["close"][-1]-pred_y[-1]
#     plt.title("{},mse:{:.2f},last diff:{:.2f}".format(test_df.index[-1].strftime("%Y%m%d"),mod.mse_total,last_diff))
#     plt.legend()
# 
#     ax5 = plt.subplot(212)
#     residual=pred_y-test_df["close"]
#     residual.plot(ax=ax5,label="residual")
#     plt.legend()
# 
#     title=prefix+":"+",".join(names)
#     plt.suptitle("predtion")
#     fpath = os.path.join("img", prefix + "_" + "_".join(names) + "_pred.png")
#     plt.savefig(fpath)
#     print(fpath)
# 
#     plt.close()



start="2020-10-31"


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

def roll_model(features,names, title):
    features = features.dropna()
    
    X = features[names]
    X = sm.add_constant(X)
    y =  features["close"]
    
    win =  60
    
    rols = RollingOLS(y,X, window=win)
    rres = rols.fit()
    params = rres.params.copy()
#     fig = rres.plot_recursive_coefficient(variables=names)
    plt.grid(True)
#     plt.show()
    
    
    df1=X[win-1:]
    df2=params.dropna()
    c = df1.dot(df2.T)
    print("c",c)
    y = y[win-1:]
    print("y",y)
    
    err = c - y
    err.to_html("err.html")
    print("err", err)
    err = err.apply(np.square)
    

    
    n = len(y)
    
    msr = []
    for i in range(-n+1,n-1):
        mean_val = np.mean(np.diag(err.to_numpy(),k=i))
        print(i,mean_val)
        msr.append(mean_val)
        
    plt.plot(range(-n+1,n-1),msr)
#     plt.show()

        
    
    print("err2",err)
        
    
    
    
    
    
    fitted = np.diagonal(c.to_numpy())
    ax = y.plot(label="close")
    plt.plot(df1.index,fitted,label="pred")
    plt.legend()
#     plt.show()
#     print(list(zip(df1.index,fitted,features[59:]["close"])))
    
    
if __name__=="__main__":
    
    for name in ["000905"]:
        features=get_features(name)
#         model(features,["lev","f1"],name)
#         print(features[-1:])
#         model(features,["lev","extra_lev","sell","extra_sell","f1"],name)
#         model(features,["lev","extra_lev","sell","extra_sell"],name)
        roll_model(features,["lev","sell"],name)
#         model(features,["total_lev","total_sell","f1"],name)


