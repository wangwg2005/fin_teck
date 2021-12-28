# -*- coding: utf-8 -*-

import os
import pandas as pd
import study.leverage.dump as dump
import statsmodels.api as sm
import mplfinance as mpf
from study.quant import datasource as ds
from study.leverage import quant_buttom_ana as quant

def batch_extract_data(sids, exchange):
    
    for sid in sids:
        s_code=sid[:6]
        apath=os.path.join("stock",s_code)
        if not os.path.exists(apath):
            os.mkdir(apath)
            
        quant.get_price(sid,os.path.join("stock",s_code,"price.csv"))
    
#     base_dir="../cache"
    
#     files =filter(lambda f:len(f)> 10 and f[6]=='_',os.listdir(base_dir))
#     
#     sids=set(map(lambda a:a[:6],files))
#     sids=["000723"]
#     
#     [os.makedirs(os.path.join("stock",sid),exist_ok=True) for sid in sids]
#     for file in files :
#         df=pd.read_json(os.path.join(base_dir,file)).set_index("day")
#         print(df.head())
#         df.to_csv(os.path.join("stock",file[:6],"price.csv"))
#     
#     sse_sids=list(filter(lambda sid:sid[0]=='6', sids))
#     szse_sids=list(filter(lambda sid:sid[0]=='0' or sid[0]=='3', sids))
#     scodes=list(map(lambda sid:sid[:6],sids))
#      
#     leve_fnames=list(map(lambda sid:os.path.join("stock",sid,"leverage.csv"),scodes))
#   
#     dump.extract_fast(scodes, exchange, leve_fnames)
    

    
def get_f(files):
    sli=slice("2019-12-31","2021-12-31")
    print("stock id:",files[0][6:12])
    price=pd.read_csv(files[0],index_col=[0],parse_dates=True)
    print(price[-3:])
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
    
    show_day=0
    
#     print(model.fittedvalues[-5:])
    
    add_plot=[mpf.make_addplot(model.fittedvalues[-show_day:],color="b"),mpf.make_addplot(model.resid[-show_day:],panel=1)]
    mpf.plot(feature[-show_day:],type="candle",volume=True,style=ds.get_style(),addplot=add_plot,title=sid,savefig=os.path.join("stock_img",sid+"n.png"))
    print("printing "+sid+" picture")
    return model
    

def train(sids):
    base_dir="stock"
#     sids=os.listdir(base_dir)
    files= map(lambda sid:(os.path.join(base_dir,sid,"price.csv"),os.path.join(base_dir,sid,"leverage.csv")) ,sids)
#     files=list(files)
#     print(files)
    features=map(get_f,files)
#     features=filter(lambda f:len(f)>200,features)
    models=map(build_model,list(zip(sids,features)))
    
    columns=["R_Squared","F_Value","F_P_value","Last Resid","Last Fitted Value","percent"]
    rows=map(lambda m:[m.rsquared,m.fvalue,m.f_pvalue,m.resid[-1],m.fittedvalues[-1],m.resid[-1]/m.fittedvalues[-1]] ,models)
    result=pd.DataFrame(list(rows),index=sids,columns=columns)
    result.index.name="sid"
    result.to_csv(os.path.join("stock_img","result_sz1.csv"))
    

    

    
    
    


if __name__=="__main__":
    
#     df=pd.read_excel("../leverage/sse/rzrqjygk20211224.xls",sheet_name=-1,index_col=[0]);
#   
#     sids=df.index
#     sids= filter(lambda id:id >600000  , sids)
#     sids = list(map(lambda id:str(id)+'.sh',sids))
# #     print(sids)
#      
#     batch_extract_data(sids,exchange="sse")
    
    
    df=pd.read_excel("../leverage/szse/rzrqjygk2021-12-24.xls",sheet_name=-1);
    sids=df['证券代码']
    sids= filter(lambda id:id <100000 and id<2008, sids)
    sids = list(map(lambda id:'{0:0>6}'.format(id),sids))
    print(sids)
#     batch_extract_data(sids,exchange="szse")
    
#     sids=list(map(lambda sid:sid[:6],sids))

#     sids=["600096"]
    train(sids)
