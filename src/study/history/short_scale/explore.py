# -*- coding: utf-8 -*-

import pandas as pd
import mplfinance as mpf
from study.quant import datasource as ds
import statsmodels.api as sm
from datetime import datetime
from study.realtime import inquery

def explor():
    df=pd.read_json("sh000905_1023_2021-11-10_15_00_00.json")
    df.index=pd.to_datetime(df.pop("day"))
    
    print(df.columns)
    
    delta=df["close"]-df["open"]
    delta=delta.map(lambda a: 1 if a>0 else -1)
    vol1=df["volume"]*delta
    df["vol1"]=vol1.cumsum()
    
    print("last day:",df["vol1"][-1])
    leng=48*20
    
    
    
    print(df)
    
    # add_plot=[mpf.make_addplot(df['vol1'],color='b')]
    
    X=df[["vol1"]]
    X=sm.add_constant(X)
    y=df["close"]
    model=sm.OLS(y,X).fit()
    print(model.summary())
    
    fitted = model.fittedvalues[-leng:]
    
    
    df=df[-leng:]
    
#     add_plot=[mpf.make_addplot(fitted,color="b"),mpf.make_addplot(model.resid[-leng:],panel=1)]
#     mpf.plot(df,type="candle",volume=True,style=ds.get_style(),addplot=add_plot)
    
    return model, df["vol1"][-1]
    
def hot_startup():
    now_v=datetime.today()
    
    open_str=now_v.strftime("%Y-%m-%d 09:30:00")
    open_time=datetime.strptime(open_str,"%Y-%m-%d %H:%M:%S")
    datelen=(now_v-open_time).seconds//300 + 1
    
    model,hotvalue=explor()
    
    if datelen>66:
        datelen=48
    elif datelen>42:
        datelen=datelen-18
    elif datelen>24:
        datelen=24
        
    result=inquery.split_time_window("sh000905", datelen)
    print(result)
    df=pd.DataFrame(result,dtype=float)
    df.index=pd.to_datetime(df.pop("day"))

    
    delta=df["close"]-df["open"]
    delta=delta.map(lambda a: 1 if a>0 else -1)
    vol1=df["volume"]*delta
    df["vol1"]=vol1.cumsum()+hotvalue
    
    X=df[["vol1"]]
    X=sm.add_constant(X)
    y_pred=model.predict(X)
    
    
    add_plot=[mpf.make_addplot(y_pred,color="b")]
    mpf.plot(df,type="candle",volume=True,style=ds.get_style(),addplot=add_plot)    
        
        
    
    
    
if __name__ =="__main__":
#     explor()
    hot_startup()