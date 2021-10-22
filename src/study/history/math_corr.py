# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import pandas as pd
from study.history import model_trainer2 as mt
import os
from scipy import stats
import statsmodels.api as sm
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


indepent_var="融资余额(亿元)"


def get_df(name):
    files=list(map(lambda a:os.path.join(name,a),mt.read_dir(name)))
        
    start="2019-12-31"
    
    split_date="2020-12-31"
    
    prices=mt.read_history(files[0])[start:]
    
    lever=mt.read_leverage(files[1])[start:]
#     lever.plot()
#     plt.show()
    
    df=prices[["收盘价"]]
    df["lev"]=lever[indepent_var]
    df=df.rename(columns={"收盘价":"price"})
    df=df.dropna()
    df=df.sort_index()
    return df[:split_date],df[split_date:]

def model_predit(model, df):
    pass


def model(name):
    df,test_df=get_df(name)
    
    
    plt.figure(figsize=(11,8))
    
    
    X=df[["lev"]]
    X["lev_2"]=X["lev"]**2
    X["lev_3"]=X["lev"]**3
    X=sm.add_constant(X)
    y=df["price"]
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
    plt.plot(df["lev"],y,'o', label='data')
    plt.plot(df["lev"],mod.fittedvalues, 'r--.',label='OLS')
    plt.title("Reg")
    plt.legend()
    
    X=test_df[["lev"]]
    X["lev_sqr"]=X["lev"]**2
    X["lev_3"]=X["lev"]**3
    X=sm.add_constant(X)
    pred_y=mod.predict(X)
    plt.legend()
    
    ax4=plt.subplot(224)
    test_df["price"].plot(ax=ax4,label="observation")
    pred_y.plot(ax=ax4,label="prediction")
    plt.title("Verify,mse:"+str(mse))
    plt.legend()
    
    plt.suptitle(name+","+indepent_var)
    plt.subplots_adjust(hspace=0.5)
    plt.savefig(r'C:\Users\Darren\Pictures\model\\'+name+"_"+indepent_var+"_order3.png")
    plt.close()
    
    


def get_coor(name):
    df=get_df(name)
    print(stats.pearsonr(df["lev"], df["price"]))
    return df.corr()
    
    
if __name__=="__main__":
    names=["000905","000300","399006","000016"]
    
    
#     model("000905")
    
    for name in names:
         model(name)
#         print(get_coor(name))
#         print(name)


