# -*- coding: utf-8 -*-

import os
import pandas as pd
import study.leverage.dump as dump
import statsmodels.api as sm
import mplfinance as mpf
from study.quant import datasource as ds
from study.leverage import quant_buttom_ana as quant
import datetime
from statsmodels.regression.linear_model import OLSResults
import business_day

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
#     print(leve_fnames)
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
    features['incre']=features['close'].diff()
    features=features.dropna()
    features['vol_sum']=features.apply(lambda r: -r['volume'] if r['incre']<0 else r['volume'], axis=1)
    
    

    
    return features[-100:]


def build_ridge_model(args):
    from sklearn.linear_model import RidgeCV
    sid,feature=args[0],args[1]
    
    print("training ride model for",sid)
    if len(feature)<10:
        print(sid,"has small data,",len(feature))
        return None
    X=feature[['vol_sum',"lev_buy",'lev_sell']]
    y=feature["close"]
    
    rm = RidgeCV(alphas=[i/10 for i in range(1,400)])
    rm.fit(X, y)
    
   
def build_model(args):
    
    sid,feature=args[0],args[1]
        
    model_path=os.path.join("model",sid+"_rolling100.pickle")
    
    if os.path.exists(model_path) and False:
        model = OLSResults.load(model_path)
    else:    
        print("training for",sid)
        if len(feature)<10:
            print(sid,"has small data,",len(feature))
            return None
    #     X=feature[['volume',"lev_buy",'lev_sell']]
        X=feature[['vol_sum',"lev_buy",'lev_sell']]
        X=sm.add_constant(X)
        y=feature["close"]
        
        model=sm.OLS(y,X).fit()
        model.save(model_path)
    
    show_day=0
    
#     print(model.fittedvalues[-5:])
#     print(model.conf_int(alpha=0.05, cols=None))
    if model.rsquared>0.8:
        print("printing "+sid+" picture")
        add_plot=[mpf.make_addplot(model.fittedvalues[-show_day:],color="b"),mpf.make_addplot(model.resid[-show_day:],panel=1)]
        mpf.plot(feature[-show_day:],type="candle",volume=True,style=ds.get_style(),addplot=add_plot,title=sid,savefig=os.path.join("stock_img",sid+"sum.png"))
        
    return model
    

def train(sids):
    base_dir="stock"
#     sids=os.listdir(base_dir)
    files= map(lambda sid:(os.path.join(base_dir,sid,"price.csv"),os.path.join(base_dir,sid,"leverage.csv")) ,sids)
#     files=list(files)
#     print(files)
    features=map(get_f,files)
#     features=filter(lambda f:len(f)>200,features)
    models=list(map(build_model,zip(sids,features)))
    
    columns=["R_Squared","F_Value","F_P_value","Last Resid","Last Fitted Value","percent","deviation"]
    
#     for i in range(-1,-30,-1):
    i=-1
    rows=map(lambda m:[m.rsquared,m.fvalue,m.f_pvalue,m.resid[i],m.fittedvalues[i],m.resid[i]/m.fittedvalues[i],m.resid[i]/(m.mse_total/(len(m.fittedvalues)**0.5))] ,models)
    result=pd.DataFrame(list(rows),index=sids,columns=columns)
    result.index.name="sid"
    today_str = str(datetime.datetime.today())[:10]
    result.to_csv(os.path.join("stock_img",f"result_rolling_{today_str}.csv"))
    

def filter_stk():
#     page_addr='C:/Users/Darren/eclipse-workspace/fin_study/src/javascript/candlestick.html?id={0:0>6}&scale=m5&value={1:0.2f}'
    page_addr='candlestick.html?id={0:0>6}&scale=m5&value={1:0.2f}'
    
    today_str = str(datetime.datetime.today())[:10]
#     today_str='2021-12-31'
#     fname = f"result_{today_str}.csv"

    days=pd.date_range(start='2021-11-01', end='2022-01-01', freq=business_day.get_business_day_cn())
#     for i in range(-1,-30,-1):
        
        
    
    df = pd.read_csv(os.path.join("stock_img",f"result_rolling_{today_str}.csv"))
    
    df = df[ (df.R_Squared>0.8) & (df.deviation<-2)]
    df['image'] = df['sid'].map(lambda t:'<a href="{0:0>6}sum.png">image</a>'.format(t))
    df['code'] = df['sid'].map(lambda c: "sh{0:0>6}".format(c) if c>600000 else "sz{0:0>6}".format(c))
    df['realtime'] = df.apply(lambda r:f'<a href="{page_addr}" target="_blank">link</a>'.format(r['code'],r['Last Fitted Value']),axis=1)
    sid=df.pop('sid')
    df.pop('code')
    
    df.index = sid.map(lambda a:'{0:0>6}'.format(a))
    df = df.sort_values(by='deviation')
    df.to_html(os.path.join("stock_img",f'result_rolling_{today_str}_target.html'),escape=False)
        
    
    
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
#     sids_sse=[]
    
    
    df=pd.read_excel("../leverage/szse/rzrqjygk2021-12-31.xls",sheet_name=-1);
    sids=df['证券代码']
    sids= filter(lambda id:id <100000 , sids)
    sids_sz = list(map(lambda id:'{0:0>6}.sz'.format(id),sids))
#     sids=["002008.sz"]
    
    skip_lever = False
    
    if not skip_lever:
        batch_extract_data(sids_sse,exchange="sse")
        batch_extract_data(sids_sz,exchange="szse")
    
    skip_price = True
    
    if not skip_price:
        
        import time
        
        sids=sids_sse + sids_sz
    
        for sid in sids:
            s_code=sid[:6]
            apath=os.path.join("stock",s_code)
            if not os.path.exists(apath):
                os.mkdir(apath)
            
            try:    
                quant.get_price(sid,os.path.join("stock",s_code,"price.csv"))
            except:
                time.sleep(8*60)
                quant.get_price(sid,os.path.join("stock",s_code,"price.csv"))
 
 

def load_proxies():
    "代理没有 用"
    test_url='https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=sh000905&scale=240&ma=no&datalen=1024'
    ips=[]
    import requests
    for i in range(1,34):
        url=f'http://www.66ip.cn/areaindex_{i}/1.html'
        proxies= pd.read_html(url)
        
        proxies = proxies[1][1:]
        urls = 'http://'+ proxies[0]+':' + proxies[1]
        
        urls = urls.drop_duplicates()
        
        
             
        for u in urls:
            try:
                res = requests.get(test_url,proxies={"http":u})
                result = res.json()
                print("good proxy:"+u)
                ips.append(u)
            except:
                print("bad proxy:"+u)
    
    today_str = str(datetime.datetime.today())[:10]
    with open('proxy'+today_str+'.txt','w') as f:
        f.writelines('\n'.join(ips))     
#         print(urls)
            
def train_all():
    sids= os.listdir("stock")
    sids=list(filter(lambda id: id[0] in ['0','6'] and id<'679999',sids))
    
    train(sids)
    

if __name__=="__main__":
#     load_proxies()
#     load_all_data()
    train_all()
    filter_stk()
#     process()

    
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
