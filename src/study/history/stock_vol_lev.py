# -*- coding: utf-8 -*-

import os
import pandas as pd
import study.leverage.dump as dump
import statsmodels.api as sm
import mplfinance as mpf
from study.quant import datasource as ds
from study.leverage import quant_buttom_ana as quant
import datetime

def batch_extract_data(sids, exchange):
    

    
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

    
    scodes=list(map(lambda sid:sid[:6],sids))
#      
    leve_fnames=list(map(lambda sid:os.path.join("stock",sid,"leverage.csv"),scodes))
#   
    dump.extract_fast(scodes, exchange, leve_fnames)
    

    
def get_f(files):
    sli=slice("2019-12-31","2021-12-31")
    print("stock id:",files[0][6:12])
    price=pd.read_csv(files[0],index_col=[0],parse_dates=True)
#     print(price[-3:])
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
#     print(model.conf_int(alpha=0.05, cols=None))
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
    
    columns=["R_Squared","F_Value","F_P_value","Last Resid","Last Fitted Value","percent","deviation"]
    rows=map(lambda m:[m.rsquared,m.fvalue,m.f_pvalue,m.resid[-1],m.fittedvalues[-1],m.resid[-1]/m.fittedvalues[-1],m.resid[-1]/(m.mse_total/(len(m.fittedvalues)**0.5))] ,models)
    result=pd.DataFrame(list(rows),index=sids,columns=columns)
    result.index.name="sid"
    today_str = str(datetime.datetime.today())[:10]
    result.to_csv(os.path.join("stock_img",f"result_{today_str}.csv"))
    

def filter_stk():
    page_addr='C:/Users/Darren/eclipse-workspace/fin_study/src/javascript/candlestick.html?id={0:0>6}&scale=m5'
    
    today_str = str(datetime.datetime.today())[:10]
#     today_str='2021-12-29'
    fname = f"result_{today_str}.csv"
    
    df = pd.read_csv(os.path.join("stock_img",fname))
    
    df = df[ (df.R_Squared>0.9) & (df.deviation<-2)]
    df['image'] = df['sid'].map(lambda t:'<a href="{0:0>6}n.png">image</a>'.format(t))
    code = df['sid'].map(lambda c: "sh{0:0>6}".format(c) if c>600000 else "sz{0:0>6}".format(c))
    df['realtime'] = code.map(lambda t:f'<a href="{page_addr}" target="_blank">link</a>'.format(t))
    sid=df.pop('sid')
    
    df.index = sid.map(lambda a:'{0:0>6}'.format(a))
    df = df.sort_values(by='deviation')
    df.to_html(os.path.join("stock_img",f'result_{today_str}_target.html'),escape=False)
        
    
    
def process():
    
    a='000008,002307,603077,600633,600691,600855,600010,601600,600151,600509,600733,002115,002467,600410,002145,002617,600773,600418,002497,000829,002326,600096,600141,000966,002234,002518,600089,600549,002407,002240,002176,600196,600111,603026'
    sids=a.split(",")
    
    sse=[]
    szse=[]
    
    for sid in sids:
        if sid[0]=='6':
            sse.append(sid+'.sh')
        else:
            szse.append(sid+'.sz')
            
    
    
    batch_extract_data(sse,exchange="sse")
    batch_extract_data(szse,exchange="szse")
    
    train(sids)

def load_all_data():
    
    
    df=pd.read_excel("../leverage/sse/rzrqjygk20211229.xls",sheet_name=-1,index_col=[0]);
     
    sids=df.index
    sids= filter(lambda id:id >600000 and id<679999, sids)
    sids_sse = list(map(lambda id:str(id)+'.sh',sids))
    
    
#     df=pd.read_excel("../leverage/szse/rzrqjygk2021-12-29.xls",sheet_name=-1);
#     sids=df['证券代码']
#     sids= filter(lambda id:id <100000 , sids)
#     sids_sz = list(map(lambda id:'{0:0>6}.sz'.format(id),sids))
#     sids=["002008.sz"]
    
    skip_lever = True
    
    if not skip_lever:
        batch_extract_data(sids_sse,exchange="sse")
#         batch_extract_data(sids_sz,exchange="szse")
    
    skip_price = False
    
    if not skip_price:
        
        sids=sids_sse
    
        for sid in sids:
            s_code=sid[:6]
            apath=os.path.join("stock",s_code)
            if not os.path.exists(apath):
                os.mkdir(apath)
                
            quant.get_price(sid,os.path.join("stock",s_code,"price.csv"))
 
 

def load_proxies():
    url='http://www.66ip.cn/areaindex_1/1.html'
    proxies= pd.read_html(url)
    
    proxies = proxies[1][1:]
    proxies[url] = 'http://'+ proxies[0]+':' + proxies[1]
    
    print(proxies[url])
            
def train_all():
    sids= os.listdir("stock")
    sids=list(filter(lambda id: id[0] in ['0','6'] and id<'679999',sids))
    
    train(sids)
    

if __name__=="__main__":
#     load_proxies()
#     train_all()
    filter_stk()
#     process()
#     load_all_data()
    
#     sids=['600597.sh']
#     
# #     df=pd.read_excel("../leverage/sse/rzrqjygk20211224.xls",sheet_name=-1,index_col=[0]);
# #     
# #     sids=df.index
# #     sids= filter(lambda id:id >600000 and id<679999, sids)
# #     sids = list(map(lambda id:str(id)+'.sh',sids))
# # #     print(sids)
# #        
#     batch_extract_data(sids,exchange="sse")
# #     sid1=sids
# #      
# #     df=pd.read_excel("../leverage/szse/rzrqjygk2021-12-24.xls",sheet_name=-1);
# #     sids=df['证券代码']
# #     sids= filter(lambda id:id <100000 , sids)
# #     sids = list(map(lambda id:'{0:0>6}.sz'.format(id),sids))
# # #     sids=["002008.sz"]
# #     print(sids)
# #      
# #     batch_extract_data(sids,exchange="szse")
# #     sids.extend(sid1)
#     sids=list(map(lambda sid:sid[:6],sids))
# 
# #     sids=["000829"]
#     train(sids)
