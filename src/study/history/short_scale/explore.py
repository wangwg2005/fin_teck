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
from study.history.short_scale import dump

def explor(sid, realtime=True):
    print(sid)
    model_path=os.path.join("model",sid+"_realtime.pickle")
    
    if os.path.exists(model_path) and not realtime:
        return rs.load(model_path),-1
        
    bl=os.path.join("data",sid+"_baseline.json")
    
    
    df = dump.dump_data(sid) 
        
    
#     df=pd.read_json(bl)
#     df.index=pd.to_datetime(df.pop("day"))
    
#     print(df.columns)
    
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
    date_str=str(datetime.today())[:10]
    add_plot=[mpf.make_addplot(fitted,color="b"),mpf.make_addplot(model.resid[-leng:],panel=1)]
    mpf.plot(df,type="candle",volume=True,style=ds.get_style(),addplot=add_plot,title=sid,savefig=os.path.join("explore","{0}_{1}.png".format(sid,date_str)))
    
    return model, df["vol1"][-1]



def explore_v2(sid):
    print(sid)
    
    now_v=datetime.today()
    
    open_str=now_v.strftime("%Y-%m-%d 09:30:00")
    open_time=datetime.strptime(open_str,"%Y-%m-%d %H:%M:%S")
   

        
    
#     df=pd.read_json(bl)
#     df.index=pd.to_datetime(df.pop("day"))
    
#     print(df.columns)
#     
#     delta=df["close"]-df["open"]
#     delta=delta.map(lambda a: 1 if a>0 else -1)
#     vol1=df["volume"]*delta
#     df["vol1"]=vol1.cumsum()
    
    
    datalen=(now_v-open_time).seconds//300 + 1
    
    if datalen>66:
        datalen=48
    elif datalen>42:
        datalen=datalen-18
    elif datalen>24:
        datalen=24
        
    train_len=48*11
    
    pred_len=datalen
    
    pred_len=48*2
    
    df = dump.dump_data(sid,scale=pred_len+train_len) 
    
    
    delta=df["close"]-df["open"]
    delta=delta.map(lambda a: 1 if a>0 else -1)
    vol1=df["volume"]*delta
    
    df["vol1"] = vol1.cumsum()
    
    print("data len",len(df))
    print("train data len",train_len)
    train_data=df[:train_len]
    pred_date=df[train_len:]
    
    # add_plot=[mpf.make_addplot(df['vol1'],color='b')]
    
    X=train_data[["vol1"]]
    X=sm.add_constant(X)
    y=train_data["close"]
    model=sm.OLS(y,X).fit()
    print(model.summary())
    
    fitted = model.fittedvalues
    
    X=pred_date[["vol1"]]
    X=sm.add_constant(X)
    y_pred=model.get_prediction(X).summary_frame()
    
    
    filled={"y1":y_pred["obs_ci_lower"].values,"y2":y_pred["obs_ci_upper"].values,"alpha":0.2}
    add_plot=[mpf.make_addplot(y_pred["mean"],color="b")]

    date_str=str(datetime.today())[:10]
#     add_plot=[mpf.make_addplot(fitted,color="b"),mpf.make_addplot(model.resid,panel=1)]
#     mpf.plot(pred_date,type="candle",volume=True,style=ds.get_style(),fill_between=filled,addplot=add_plot,title=sid,savefig=os.path.join("explore","{0}_realtime_v2.png".format(sid,date_str)))
    mpf.plot(pred_date,type="candle",volume=True,style=ds.get_style(),fill_between=filled,addplot=add_plot,title=sid)
    
#     return model, df["vol1"][-1]

def get_hot_data(sid):
    today_str=str(datetime.today())[:10]
    days=pd.date_range(end=today_str,periods=5, freq=bd.get_business_day_cn("all"))[:-1]
    print(days)
    fnames=[ os.path.join("data",sid+ '_' +str(day)[:10]+".hd") for day in days[::-1]]
    cnt=0
    for fname in fnames:
        if os.path.exists(fname):
            print("get hot value from date:",fname[14:24])
            with open(fname,"r") as f:
                return float(f.readline()),cnt
        else:
            cnt+=1
            
    return 0,0;
    
def hot_startup(sid):
    now_v=datetime.today()
    
    open_str=now_v.strftime("%Y-%m-%d 09:30:00")
    open_time=datetime.strptime(open_str,"%Y-%m-%d %H:%M:%S")
    datalen=(now_v-open_time).seconds//300 + 1
    
    model,hd=explor(sid,realtime=False)
    
    hotvalue,time_delta = get_hot_data(sid)
    print("time dalta",time_delta)
    
    
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

    result=inquery.split_time_window(sid, datalen+time_delta*48)
    print(result)
    
    df=pd.DataFrame(result,dtype=float)
    df.index=pd.to_datetime(df.pop("day"))

    
    delta=df["close"]-df["open"]
    delta=delta.map(lambda a: 1 if a>0 else -1)
    vol1=df["volume"]*delta
    df["vol1"]=vol1.cumsum()+hotvalue
    if datalen==48:
        with open(os.path.join("data",sid+'_'+str(now_v)[:10]+".hd"),"w") as f:
            f.write(str(df["vol1"][-1]))
        fname=(os.path.join("data",sid+"_"+str( datalen+time_delta*48)+"_"+str(df.index[-1])+".json")).replace(" ", "_").replace(":", "_")
        with open(fname,"w",encoding="utf8") as f:
            json.dump(result,f)
    
    
    X=df[["vol1"]]
    X=sm.add_constant(X)
    y_pred=model.get_prediction(X).summary_frame()
    
    filled={"y1":y_pred["obs_ci_lower"].values,"y2":y_pred["obs_ci_upper"].values,"alpha":0.2}
    add_plot=[mpf.make_addplot(y_pred["mean"],color="b")]
    mpf.plot(df,type="candle",volume=True,style=ds.get_style(),addplot=add_plot,fill_between=filled,title=sid)    
#     plt.close()

    
    
        
def explorer():    
    date_str="2021-11-17"
    base_dir="../../cache/"+date_str
     
    file1=base_dir+"_incr.csv"
    file2=base_dir+"_ratio.csv"
    columns=["R_Squared","F_Value","F_P_value","Last Resid"]
    result=pd.DataFrame()
    
    index=[]
    for f in [file1,file2]:
     
        df=pd.read_csv(f,index_col=[0])
        sids = list(map(inquery.convert_sid,df.index))
        index.extend(sids)
        models=map(explor,sids)
        rows=map(lambda m:[m[0].rsquared,m[0].fvalue,m[0].f_pvalue,m[0].resid[-1]] ,models)
        result=result.append(list(rows),ignore_index=True)
    
#     print(index)
    result.index=index
    result.index.name="sid"
    result.columns=columns
#     print(result)
    result=result.sort_values(by=['R_Squared'], ascending=False)
    result.to_csv("result{0}.csv".format(date_str))
    
if __name__ =="__main__":
#     explorer()
    
#     from study.leverage import leverage_reader as lr
#     explor("sz002176")
#     hot_startup("sh600333")

#         
#     
#     print(df1)
#     explor("sz002176")
#     explor("sh600277")
#     hot_startup('sh000905')
#     explore_v2("sh600958")
    explore_v2("sh000905")
#     explore_v2("sh601669")
#     explor("sh601669")
#     explor("sz002714")
#     explor("sz002405")
#     explor("sz399006")
#     explor("sz300998")
#     explor("sh600115")
#     explor("sh601606")
    
#     explor("sz002371")
#     explor("sz002118")
    