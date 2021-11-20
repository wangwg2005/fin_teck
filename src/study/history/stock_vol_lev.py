# -*- coding: utf-8 -*-

import os
import pandas as pd
import study.leverage.dump as dump
import statsmodels.api as sm
import mplfinance as mpf
from study.quant import datasource as ds

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
    
def get_f(files):
    sli=slice("2019-12-31","2021-12-31")
    print("stock id:",files[0][6:12])
    price=pd.read_csv(files[0],index_col=[0],parse_dates=True)
    lev_df=pd.read_csv(files[1],index_col=[0],parse_dates=True)
    features=price
    features["lev_buy"]=lev_df["融资余额(元)"]
    features["lev_sell"]=lev_df["融券余量"]
    features=features.dropna()

    
    return features[sli]
    
   
def build_model(args):
    
    sid,feature=args[0],args[1]
    if len(feature)<10:
        print(sid,"has small data,",len(feature))
        return None
    X=feature[['volume',"lev_buy",'lev_sell']]
    X=sm.add_constant(X)
    y=feature["close"]
    
    model=sm.OLS(y,X).fit()
    
    add_plot=[mpf.make_addplot(model.fittedvalues,color="b"),mpf.make_addplot(model.resid,panel=1)]
    mpf.plot(feature,type="candle",volume=True,style=ds.get_style(),addplot=add_plot,title=sid,savefig=os.path.join("stock_img",sid+".png"))
    return model
    

def train():
    base_dir="stock"
    sids=os.listdir(base_dir)
    files= map(lambda sid:(os.path.join(base_dir,sid,"price.csv"),os.path.join(base_dir,sid,"leverage.csv")) ,sids)
#     files=list(files)
#     print(files)
    features=map(get_f,files)
    features=filter(lambda f:len(f)>200,features)
    models=map(build_model,list(zip(sids,features)))
    
    columns=["R_Squared","F_Value","F_P_value","Last Resid"]
    rows=map(lambda m:[m.rsquared,m.fvalue,m.f_pvalue,m.resid[-1]] ,models)
    result=pd.DataFrame(list(rows),index=sids,columns=columns)
    result.index.name="sid"
    result.to_csv(os.path.join("stock_img","result.csv"))
    

    

    
    
    


if __name__=="__main__":
    train()
#     batch_extract_data()
