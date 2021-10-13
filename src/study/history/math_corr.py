# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import pandas as pd
from study.history import model_trainer2 as mt
import os
from scipy import stats
import statsmodels.api as sm
import seaborn as sns
import matplotlib.pyplot as plt


def get_df(name):
    files=list(map(lambda a:os.path.join(name,a),mt.read_dir(name)))
    
    sli=slice("2014-12-31","2020-12-31")
    
    prices=mt.read_history(files[0])[sli]
    
    lever=mt.read_leverage(files[1])[sli]
    
    df=prices[["收盘价"]]
    df["lev"]=lever["融资余额(亿元)"]
    df=df.rename(columns={"收盘价":"price"})
    df=df.dropna()
    df=df.sort_index()
    return df

def model(name):
    df=get_df(name)
    
    sns.regplot(x="lev",y="price",data=df)
    plt.show()

    X=df[["lev"]]
    X=sm.add_constant(X)
    y=df["price"]
    mod=sm.OLS(y,X).fit()
    print(mod.summary())
    
    pred=y-mod.resid
    
    ax=mod.resid.plot()
    pred.plot(ax=ax)
    y.plot(ax=ax)
    
    
    
    z, p = stats.normaltest(mod.resid.values)
    print("p-value",p)
    
#     plt.close()
#     plt.hist(mod.resid.values,100)
    
#     plt.plot(df["lev"],y,'o', label='data')
#     plt.plot(df["lev"],mod.fittedvalues, 'r--.',label='OLS')
    plt.show()
    
    


def get_coor(name):
    df=get_df(name)
    print(stats.pearsonr(df["lev"], df["price"]))
    return df.corr()
    
    
if __name__=="__main__":
    names=["000905","000300","399006","000016"]
    
    
    model("000300")
    
#     for name in names:
#         
#         print(get_coor(name))
#         print(name)


