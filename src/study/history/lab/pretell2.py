# -*- coding: utf-8 -*-

import os
import pandas as pd
from statsmodels.regression.linear_model import RegressionResults as rs
import statsmodels.api as sm
import mplfinance as mpf
from study.quant import datasource as ds

def get_feature(sid):
#     print("sid:",sid)
    base_dir=r"../../leverage/cache"
    price=pd.read_csv(os.path.join(base_dir,sid+".csv"),index_col=[0],parse_dates=True)
    lev_df=pd.read_csv(os.path.join("data","leverage",sid+".csv"),index_col=[0],parse_dates=True)
    features=price
    features["lev_buy"]=lev_df["融资余额(元)"]
    features["lev_sell"]=lev_df["融券余量"]
    features=features.dropna()
    
    return features

def batch_predict():
    mlist=pd.read_csv(os.path.join("img","result.csv"),dtype={"sid":object})
    target=mlist[mlist['R_Squared']>0.8]
    sids=list(map(lambda sid:sid.rjust(6,"0"),target["sid"].values))
    base_dir=r"../../leverage/cache"
#     files=map(lambda sid:(sid,os.path.join(base_dir,sid)),sids)
    dfs=map(lambda f:(f,get_feature(f)),sids)
#     dfs=list(dfs)
#     print(dfs[0])
#     print(len(dfs))
#     dfs=filter(lambda df:len(df[1])>1000,dfs)


    dfs=map(lambda df:(df[0],df[1]["2021-01-04":]),dfs)
    
    result=pd.DataFrame(columns=["sid","diff","ratio"])
    
    for sid,df in dfs:
        print("predicting",sid)
        model=rs.load(os.path.join("model",sid+".pickle"))
        X=df[['volume',"lev_buy",'lev_sell']]
        X=sm.add_constant(X)
        y_pred=model.get_prediction(X).summary_frame()
        add_plot=[mpf.make_addplot(y_pred["mean"],color="b")]
        filled=dict(y1=y_pred["obs_ci_lower"].values,y2=y_pred["obs_ci_upper"],alpha=0.2)
        mpf.plot(df,type="candle",volume=True,style=ds.get_style(),addplot=add_plot,fill_between=filled,title=sid,savefig=os.path.join("pred",sid+".png"))
        last_pred=y_pred["mean"][-1]
        last_obs=df["close"][-1]
        r={"sid":sid,"diff":last_pred-last_obs,"ratio":last_pred/last_obs-1}
        result=result.append(r,ignore_index=True)
        
    result=result.set_index("sid")
    result=result.sort_values(by="ratio")
    print(result)
    result.to_csv(os.path.join("pred","pred.csv"))

if __name__ == "__main__":
    batch_predict()