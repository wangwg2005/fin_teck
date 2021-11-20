# -*- coding: utf-8 -*-

import os
import pandas as pd
import study.leverage.dump as dump
import statsmodels.api as sm
import mplfinance as mpf
from study.quant import datasource as ds
import study.leverage.leverage_reader as lr
from statsmodels.regression.linear_model import RegressionResults as rs
from study.realtime import price_query as pq
import time

def batch_extract_data():
    
    base_dir="../cache"
    
    files =filter(lambda f:len(f)> 10 and f[6]=='_',os.listdir(base_dir))
    
    sids=set(map(lambda a:a[:6],files))
#     
#     [os.makedirs(os.path.join("stock",sid),exist_ok=True) for sid in sids]
#     for file in files :
#         df=pd.read_json(os.path.join(base_dir,file)).set_index("day")
#         print(df.head())
#         df.to_csv(os.path.join("stock",file[:6],"price.csv"))
#     
    sse_sids=list(filter(lambda sid:sid[0]=='6', sids))
    szse_sids=list(filter(lambda sid:sid[0]=='0' or sid[0]=='3', sids))
     
    sse_leves=list(map(lambda sid:os.path.join("stock",sid,"leverage.csv"),sse_sids))
  
    dump.extract_fast(sse_sids, "sse", sse_leves)
     
#     szse_leves=list(map(lambda sid:os.path.join("stock",sid,"leverage.csv"),szse_sids))
#     dump.extract_fast(szse_sids, "szse", szse_leves)
    
def get_feature(sid):
#     print("sid:",sid)
    base_dir=r"../../leverage/cache"
    price=pd.read_csv(os.path.join(base_dir,sid+"_2020.csv"),index_col=[0],parse_dates=True)
    lev_df=pd.read_csv(os.path.join("data","leverage",sid+".csv"),index_col=[0],parse_dates=True)
    features=price
    features["lev_buy"]=lev_df["融资余额(元)"]
    features["lev_sell"]=lev_df["融券余量"]
    features=features.dropna()

    
    return features
    
   
def build_model(args):

    
    sid,feature=args[0],args[1]
    
    fpath=os.path.join("model",sid+".pickle")
    if os.path.exists(fpath):
        return rs.load(fpath)
    print("building model for ",sid)
    if len(feature)<10:
        print(sid,"has small data,",len(feature))
        return None
    X=feature[['Volume',"lev_buy",'lev_sell']]
    X=sm.add_constant(X)
    y=feature["Close"]
    
    model=sm.OLS(y,X).fit()
    
    add_plot=[mpf.make_addplot(model.fittedvalues,color="b"),mpf.make_addplot(model.resid,panel=1)]
    mpf.plot(feature,type="candle",volume=True,style=ds.get_style(),addplot=add_plot,title=sid,savefig=os.path.join("img",sid+".png"))
    model.save(fpath)
    return model
    

def train():
    base_dir=r"../../leverage/cache"
    df=pd.read_csv("stock_id.csv",index_col=[0])
    sid_all=[ sid[:6] for sid in df.index]
    files=os.listdir(base_dir)
    
    
    files= filter(lambda file: file[7:]=='2020.csv' and file[:6] in sid_all,files)
    sids=list(map(lambda file:file[:6],files))
#     files=list(files)
#     print(files)
    features=map(get_feature,sids)
#     features=filter(lambda f:len(f)>200,features)
    models=map(build_model,list(zip(sids,features)))
    
    columns=["R_Squared","F_Value","F_P_value","Last Resid"]
    rows=map(lambda m:[m.rsquared,m.fvalue,m.f_pvalue,m.resid[-1]] ,models)
    result=pd.DataFrame(list(rows),index=sids,columns=columns,dtype=str)
    
    result.index.name="sid"
    result=result.sort_values(by=["R_Squared","Last Resid"],ascending=[False,True])
    result.to_csv(os.path.join("img","result.csv"))
    

    

    
def get_id_list():
    baseline_date="2021-11-17"
    sse_df=lr.read_detail_sse(baseline_date)
    sse_df=sse_df[sse_df.index.str.startswith("60")]
    index=list(sse_df.index)
    values=list(sse_df['标的证券简称'].values)
    
    szse_df=lr.read_detail_szse(baseline_date)
    szse_df=szse_df[szse_df.index.str.startswith("00")]
    index.extend(list(szse_df.index))
    values.extend(list(szse_df['证券简称'].values))
    
    df=pd.DataFrame({"证券简称":values},index=index)
    df.index.name="证券代码"
    df.to_csv("stock_id.csv")
#     df=pd.DataFrame()
#     df.index.name="证券代码"
#     szse_df=lr.read_detail_szse(baseline_date)[["证券简称"]]
#     df=df.append(szse_df.loc['000001.SZ'])
    
#     print(df)
    
def get_price():
    df=pd.read_csv("stock_id.csv",index_col=[0])
    df=df['600346.SS':]
    
    base_dir=r"../../leverage/cache"
    
    files=map(lambda sid:(sid,os.path.join(base_dir,sid[:6]+".csv")), df.index)
    files=filter(lambda f: not os.path.exists(f[1]),files)
    for sid, file in files:
        print("downloading ",sid)
        nid=pq.convert_sid(sid)
        print("retriving data for",sid)
        time.sleep(30)
        result=pq.get_history_price(nid)
        ndf=pd.DataFrame(result)
        ndf.set_index("day") 
        ndf.to_csv(file)
        
    
    print("data download finished")
    
def get_leverage():
    df=pd.read_csv("stock_id.csv",index_col=[0])

    
    base_dir="data/leverage"
#     sse=df[df.index.str.endswith("SS")]
#     sids=list(map(lambda sid:sid[:6],sse.index))
#     paths=list(map(lambda sid:os.path.join(base_dir,sid+".csv"),sids))
#     dump.extract_fast(sids, "sse", paths)
    
    szse=df[df.index.str.endswith("SZ")]
    sids=list(map(lambda sid:sid[:6],szse.index))
    paths=list(map(lambda sid:os.path.join(base_dir,sid+".csv"),sids))
    dump.extract_fast(sids, "szse", paths)
    
    

if __name__=="__main__":
    get_price()
#     get_leverage()
#     get_id_list()
#     train()
#     batch_extract_data()
