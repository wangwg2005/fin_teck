# -*- coding: utf-8 -*-
import pandas as pd
import os
from scipy import stats
import statsmodels.api as sm
import matplotlib.pyplot as plt

def get_features(name):
    
    price_df=pd.read_csv(os.path.join(name,name+".csv"),encoding="utf8",parse_dates=[0],index_col=0,header=0,nrows=1000)
    print(price_df)
    return price_df
    
    
def model(feature):
    print(feature.dtypes)
    feature["f1"]=feature["成交量"]*feature["涨跌幅"].map(lambda a: 1 if a>0 else -1)/10000000
    print(feature)
    print(feature.corr()["f1"])
    feature["f2"]=feature["涨跌幅"].map(lambda a: a if a>0 else -a)
    plt.scatter(feature["成交量"],feature["涨跌幅"])
#     
#     X=feature[["f1"]]
#     X=sm.add_constant(X)
#      
#     m=sm.OLS(feature["收盘价"],X).fit()
#     print(m.summary())
#      
#     ax=feature["收盘价"].plot()
#     m.fittedvalues.plot(ax=ax,label="fitted")
    plt.show()
    
    
    
if __name__=="__main__":
    feature = get_features("000905")["2019-12-31":'2020-12-31']
    model(feature)