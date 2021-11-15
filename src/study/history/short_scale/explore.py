# -*- coding: utf-8 -*-

import pandas as pd
import mplfinance as mpf
from study.quant import datasource as ds
import statsmodels.api as sm
from datetime import datetime
from study.realtime import inquery
import business_day as bd
import os
import json
from statsmodels.regression.linear_model import RegressionResults as rs

def explor(sid):
    
    model_path=sid+"_realtime.pickle"
    if os.path.exists(model_path):
        return rs.load(model_path),-1
        
    
    df=pd.read_json(sid+"_baseline.json")
    df.index=pd.to_datetime(df.pop("day"))
    
    print(df.columns)
    
    delta=df["close"]-df["open"]
    delta=delta.map(lambda a: 1 if a>0 else -1)
    vol1=df["volume"]*delta
    df["vol1"]=vol1.cumsum()
    
    leng=48*20
    
    
    # add_plot=[mpf.make_addplot(df['vol1'],color='b')]
    
    X=df[["vol1"]]
    X=sm.add_constant(X)
    y=df["close"]
    model=sm.OLS(y,X).fit()
    print(model.summary())
    model.save(model_path)
    
    fitted = model.fittedvalues[-leng:]
    
    
    df=df[-leng:]
    
    add_plot=[mpf.make_addplot(fitted,color="b"),mpf.make_addplot(model.resid[-leng:],panel=1)]
    mpf.plot(df,type="candle",volume=True,style=ds.get_style(),addplot=add_plot)
    
    return model, df["vol1"][-1]

def get_hot_data(sid):
    today_str=str(datetime.today())[:10]
    days=pd.date_range(end=today_str,periods=5, freq=bd.get_business_day_cn("all"))[:-1]
    fnames=[ sid+ '_' +str(day)[:10]+".hd" for day in days[::-1]]
    for fname in fnames:
        if os.path.exists(fname):
            print("get hot value from date:",fname[9:19])
            with open(fname,"r") as f:
                return float(f.readline())
            
    return 0;
    
def hot_startup(sid):
    now_v=datetime.today()
    
    open_str=now_v.strftime("%Y-%m-%d 09:30:00")
    open_time=datetime.strptime(open_str,"%Y-%m-%d %H:%M:%S")
    datalen=(now_v-open_time).seconds//300 + 1
    
    model,hd=explor(sid)
    
    hotvalue = get_hot_data(sid)
    
    
    if hotvalue==0:
        hotvalue=hd
        
    print("hot value:",hotvalue)
    
    if datalen>66:
        datalen=48
    elif datalen>42:
        datalen=datalen-18
    elif datalen>24:
        datalen=24
        
#     sid="sh000905"
        
    result=inquery.split_time_window(sid, datalen)
    df=pd.DataFrame(result,dtype=float)
    df.index=pd.to_datetime(df.pop("day"))

    
    delta=df["close"]-df["open"]
    delta=delta.map(lambda a: 1 if a>0 else -1)
    vol1=df["volume"]*delta
    df["vol1"]=vol1.cumsum()+hotvalue
    if datalen==48:
        with open(sid+'_'+str(now_v)[:10]+".hd","w") as f:
            f.write(str(df["vol1"][-1]))
        fname=(sid+"_48_"+str(df.index[-1])+".json").replace(" ", "_").replace(":", "_")
        with open(fname,"w",encoding="utf8") as f:
            json.dump(result,f)
    
    
    X=df[["vol1"]]
    X=sm.add_constant(X)
    y_pred=model.get_prediction(X).summary_frame()
    
    
    add_plot=[mpf.make_addplot(y_pred[["mean","obs_ci_lower","obs_ci_upper"]],color="b")]
    mpf.plot(df,type="candle",volume=True,style=ds.get_style(),addplot=add_plot)    
        
        
    
    
    
if __name__ =="__main__":
#     explor("sh000300")
    hot_startup('sh000905')