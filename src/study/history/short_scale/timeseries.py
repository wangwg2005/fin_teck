# -*- coding: utf-8 -*-

import pandas as pd
import statsmodels.api as sm
from study.history.short_scale import dump
import mplfinance as mpf
from study.quant import datasource as ds
import os
import numpy as np



def ts_model(df,train_num=5*48,pred_num=1):
    
    size=len(df)
    delta=df["close"]-df["open"]
    delta=delta.map(lambda a: 1 if a>0 else -1)
    vol1=df["volume"]*delta
    df["vol1"]=vol1.cumsum()
    X=df[["vol1"]]
    
    X=sm.add_constant(X)
    
    y=df["close"]
    
    result=pd.DataFrame()
    
    for i in range(0,size-train_num):
        sli=slice(i,i+train_num)
        model=sm.OLS(y[sli],X[sli]).fit()
        a=X[i+train_num:i+train_num+pred_num]
        y_pred=model.get_prediction(a).summary_frame()
        row = y_pred.iloc[0]
        result=result.append(row)

        
    return result

if __name__ == "__main__":
#     dataset=dump.dump_data("sh601669")
    
    dataset=dump.dump_data("sh000905")
#     dataset=dump
#     dataset=pd.read_json("data\\sh000905_baseline.json")
#     dataset.index=pd.to_datetime(dataset.pop("day"))
#     print('dataset')
#     print(dataset)
    
    
    show_num=5*48
    for train_len in [5,10,15]:
        y_pred = ts_model(dataset,train_num=train_len*48)[-show_num:]
        
        filled={"y1":y_pred["obs_ci_lower"].values,"y2":y_pred["obs_ci_upper"].values,"alpha":0.2}
#         add_plot.append(mpf.make_addplot(y_pred["mean"]))
        dataset[str(train_len)]=y_pred["mean"]
        print("loop for train day = ", train_len)
        add_plot=[mpf.make_addplot(y_pred["mean"])]
        print(y_pred["mean"])
        mpf.plot(dataset[-show_num:],type="candle",volume=True,style=ds.get_style(),addplot=add_plot,title="sh000905",fill_between=filled,savefig=os.path.join("explore","sh000905_{0}_timeseries.png".format(train_len)))
        
    dataset = dataset[-show_num:]

    add_plot=[mpf.make_addplot(dataset["5"]),mpf.make_addplot(dataset["10"]),mpf.make_addplot(dataset["15"])]
#     add_plot=[mpf.make_addplot(fitted,color="b"),mpf.make_addplot(model.resid,panel=1)]
#     mpf.plot(pred_date,type="candle",volume=True,style=ds.get_style(),fill_between=filled,addplot=add_plot,title=sid,savefig=os.path.join("explore","{0}_realtime_v2.png".format(sid,date_str)))
    mpf.plot(dataset,type="candle",volume=True,style=ds.get_style(),addplot=add_plot,title="sh000905")
  

        
        
    