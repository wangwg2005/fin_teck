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
from study.ml import cycle_test as ct

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
    print("stock id:",files[0][6:12])
    price=pd.read_csv(files[0],index_col=[0],parse_dates=True)

#     print(price[-3:])
    lev_df=pd.read_csv(files[1],index_col=[0],parse_dates=True)
    features=price
    features["lev_buy"]=lev_df["融资余额(元)"]
    features["lev_sell"]=lev_df["融券余量"]
    features['incre']=features['close'].diff()
    features=features.dropna()
    features['vol_']=features.apply(lambda r: -r['volume'] if r['incre']<0 else r['volume'], axis=1)
    features['vol_sum']=features['vol_'].cumsum()
    
    return features[-30:]
    
    

    


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
    
    
    
def lev_model(args):
    
    sid,feature=args[0],args[1]
        
    model_path=os.path.join("model",sid+"_lev.pickle")
    
    if os.path.exists(model_path) and False:
        model = OLSResults.load(model_path)
    else:    
        print("training lev model for",sid)
        if len(feature)<10:
            print(sid,"has small data,",len(feature))
            return None
    #     X=feature[['volume',"lev_buy",'lev_sell']]
        X=feature[["lev_buy",'lev_sell']]
        X=sm.add_constant(X)
        y=feature["close"]
        
        model=sm.OLS(y,X).fit()
#         model.save(model_path)
    
    show_day=0
    
#     print(model.fittedvalues[-5:])
#     print(model.conf_int(alpha=0.05, cols=None))
#     if model.rsquared>0.8:
#         print("printing "+sid+" picture")
#         add_plot=[mpf.make_addplot(model.fittedvalues[-show_day:],color="b"),mpf.make_addplot(model.resid[-show_day:],panel=1)]
#         mpf.plot(feature[-show_day:],type="candle",volume=True,style=ds.get_style(),addplot=add_plot,title=sid,savefig=os.path.join("stock_img",'img',sid+"_lev.png"))
        
    return model

    
    
def mv_model(args):
    
    sid,feature=args[0],args[1]
        
    model_path=os.path.join("model",sid+"_mv.pickle")
    
    if os.path.exists(model_path) and False:
        model = OLSResults.load(model_path)
    else:
        print("training mv model for",sid)
        if len(feature)<10:
            print(sid,"has small data,",len(feature))
            return None
    #     X=feature[['volume',"lev_buy",'lev_sell']]
        X=feature[['vol_sum']]
        X=sm.add_constant(X)
        y=feature["close"]
        
        model=sm.OLS(y,X).fit()
#         model.save(model_path)
    
    show_day=0
    
#     print(model.fittedvalues[-5:])
#     print(model.conf_int(alpha=0.05, cols=None))
#     if model.rsquared>0.8:
#         print("printing "+sid+" picture")
#         add_plot=[mpf.make_addplot(model.fittedvalues[-show_day:],color="b"),mpf.make_addplot(model.resid[-show_day:],panel=1)]
#         mpf.plot(feature[-show_day:],type="candle",volume=True,style=ds.get_style(),addplot=add_plot,title=sid,savefig=os.path.join("stock_img",'img',sid+"_mv.png"))
        
    return model
    
   
def comp_model(args):
    
    sid,feature=args[0],args[1]
    
    model_path=os.path.join("model",sid+"_comp.pickle")
    
    if os.path.exists(model_path) and False:
        model = OLSResults.load(model_path)
    else:
        print("training comp model for",sid)
        if len(feature)<10:
            print(sid,"has small data,",len(feature))
            return None
    #     X=feature[['volume',"lev_buy",'lev_sell']]
        X=feature[['vol_sum',"lev_buy",'lev_sell']]
        X=sm.add_constant(X)
        y=feature["close"]
        
        model=sm.OLS(y,X).fit()
#         print(model.summary())
#         model.save(model_path)
    
    show_day=0
    
#     print(model.fittedvalues[-5:])
#     print(model.conf_int(alpha=0.05, cols=None))
#     if model.rsquared>0.8:
#         print("printing "+sid+" picture")
#         add_plot=[mpf.make_addplot(model.fittedvalues[-show_day:],color="b"),mpf.make_addplot(model.resid[-show_day:],panel=1)]
#         mpf.plot(feature[-show_day:],type="candle",volume=True,style=ds.get_style(),addplot=add_plot,title=sid,savefig=os.path.join("stock_img",'img',sid+"_comp.png"))
        
    return model
    
import io 

def train(sids):
    base_dir="stock"
#     sids=os.listdir(base_dir)
    files= map(lambda sid:(os.path.join(base_dir,sid,"price.csv"),os.path.join(base_dir,sid,"leverage.csv")) ,sids)
#     files=list(files)
#     print(files)
    features=map(get_f,files)
#     features=filter(lambda f:len(f)>200,features)

    sf = list(zip(sids,features))
    cs = 'open,high,low,close,volume'.split(",")
    cycle_results = list( map(lambda a: ct.test_df(a[1][cs]),sf))
    cycle_df= pd.DataFrame(cycle_results,index = sids)
    print(cycle_df.head())
    
    
    columns2=["R_Squared","F_Value","F_P_value","Last Resid","Last Fitted Value","percent","deviation",'params']
    
    for model_fun in [comp_model,mv_model,lev_model]:
#     for model_fun in [mv_model]:
        
        models=map(model_fun,sf)
        
        
        
    #     for i in range(-1,-30,-1):
        i=-1
        rows=map(lambda m:[m.rsquared,m.fvalue,m.f_pvalue,m.resid[i],m.fittedvalues[i],m.resid[i]/m.fittedvalues[i],m.resid[i]/(m.mse_resid**0.5),m.params] ,models)
        result=pd.DataFrame(list(rows),index=sids,columns=columns2)
        result = pd.concat([result,cycle_df], axis=1)
        result.index.name="sid"
        today_str = str(datetime.datetime.today())[:10]
        result.to_csv(os.path.join("stock_img",f"model_param_{today_str}_{model_fun.__name__[:-6]}.csv"))
        
        
        
#         rows = map(lambda m :[m.rsquared,m.fittedvalues, m.resid+m.fittedvalues],models)
#         result = pd.DataFrame(list(rows),index = sids, columns=["R_Squared","Resid","Observation"])
#         result.index.name="sid"
#         buffer = result.to_json()
#         with open(os.path.join("stock_img",f"model_fit_{today_str}_{model_fun.__name__[:-6]}.js"),"w") as fo:
#             fo.write("fitted = ")
#             fo.write(buffer)
    

def filter_stk():
#     page_addr='C:/Users/Darren/eclipse-workspace/fin_study/src/javascript/candlestick.html?id={0:0>6}&scale=m5&value={1:0.2f}'
#     page_addr='candlestick.html?id={0:0>6}&scale=m5&value={1:0.2f}'
    
    link='<a href="candlestick.html?id={0}&scale=m5&value={1:0.2f}" target="_blank">link</a>'
    
    today_str = str(datetime.datetime.today())[:10]
#     today_str='2022-04-15'
#     fname = f"result_{today_str}.csv"

#     days=pd.date_range(start='2021-11-01', end='2022-01-01', freq=business_day.get_business_day_cn())
#     for i in range(-1,-30,-1):
        
    types=['comp','mv','lev']
    
    for t in types:
        
        print(f"generating report for {today_str} {t}")
    
        df = pd.read_csv(os.path.join("stock_img",f"model_param_{today_str}_{t}.csv"))
        
        df = df.sort_values(by ="R_Squared",ascending=True)
#         df = df[ (df.R_Squared>0.85) & (df.percent <-0.05) & (df.deviation<-2)]
        if len(df)==0:
            print(f"no qualified data for {t}!")
            continue
        
        df['code'] = df['sid'].map(lambda c: "sh{0:0>6}".format(c) if c>600000 else "sz{0:0>6}".format(c))
        df['lev'] = df['code'].map(lambda code:f'<a href="lev.html?id={code}" target="_blank">lev</a>')
        ss = df.apply(lambda r: link.format(r['code'],r['Last Fitted Value']),axis=1)
        df['realtime']  = ss
        sid=df.pop('sid')
        
        
        df.index = sid.map(lambda a:'{0:0>6}'.format(a))
        df = df.sort_values(by='percent')
        base_dir = '../../javascript/js/data'
#         report_path = os.path.join(base_dir, f'report_{today_str}_{t}.html')
        
        
        buffer = df.to_json(orient="records")
        with open( os.path.join(base_dir,f'report_{today_str}_{t}.js'),'w') as fo:
            fo.write('records = ')
            fo.write(buffer)
#         df.pop('code')
#         df.to_html(report_path,escape=False)
        

        
    
    
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
    
def get_stocks():
    
    files = os.listdir("stock_img")
    
    files = list(filter(lambda f: 'model_param'==f[:11],files))
    files.sort()
    
    f = files[-1][:23];
    
    ids= []
    
    for  tp in ["comp","mv","lev"]:
        
    

        df = pd.read_csv(os.path.join("stock_img",f+tp+".csv"))
        df = df[ (df.R_Squared>0.6)]
        ids.extend( list(df['sid'].map(lambda c: "{0:0>6}".format(c))))
        
    ids = set(ids) 
    ids = list(map(lambda id: id+".sh" if id[0]=='6' else id+".sz",ids))
    ids.sort()
    return list(ids)
    
    

def load_all_data(skip_lever = True ,skip_price = False,ids=[]):    
    sids_all=[]
    
    
    if ids != None and len(ids) > 0 :
        sids_all = ids
        sids_sse = list(filter(lambda id:id[-2:]=='sh',ids))
        sids_sz = list(filter(lambda id:id[-2:]=='sz',ids))
    
    else:
        df=pd.read_excel("../leverage/sse/rzrqjygk20220110.xls",sheet_name=-1,index_col=[0]);
          
        sids=df.index
        sids= filter(lambda id:id >600000 and id<679999 and id!=600072, sids)
        sids_sse = list(map(lambda id:str(id)+'.sh',sids))
        sids_all.extend(sids_sse)
    #     sids_sse=[]
        
        
        df=pd.read_excel("../leverage/szse/rzrqjygk2022-01-10.xls",sheet_name=-1);
        sids=df['证券代码']
        sids= filter(lambda id:id <100000 , sids)
        sids_sz = list(map(lambda id:'{0:0>6}.sz'.format(id),sids))
        sids_all.extend(sids_sz)
#     sids_sz=[]
    

    print("ids",sids_all)
    if not skip_lever:
        batch_extract_data(sids_sse,exchange="sse")
        batch_extract_data(sids_sz,exchange="szse")
    
    
    
    cnt=0
    
    if not skip_price:
        
        import time
    
        for sid in sids_all:
            s_code=sid[:6]
            apath=os.path.join("stock",s_code)
            if not os.path.exists(apath):
                os.mkdir(apath)
                
            cnt += 1
            
#             if cnt  %100 == 0:
#                 time.sleep(3*60)
            
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
            
def train_all(ids=[]):
    if ids!=None and len(ids)>0:
        sids=[id[:6] for id in ids]
    else:
        sids= os.listdir("stock")
        sids=list(filter(lambda id: id[0] in ['0','6'] and id<'679999',sids))
#     sids=['000008']
#     clean(sids)
    train(sids)
    
def clean(ids):
#     aid = list(filter(lambda id: id[-2:]=="sh",ids))
#     print(aid)
    
    for id in ids:
#         id = id[:6]
        apath=os.path.join("stock",id,"leverage.csv")
        lev = pd.read_csv(apath,index_col=[0])
#         if len(lev.columns)==7:
#             print(id)
#             df = lev.drop(lev.columns[0],axis=1)
#             df.to_csv(apath)
            
        lev2 =lev.drop_duplicates()
        if len(lev) == len(lev2) :
            print(id,"is good")
        else:
            print(id,"is bad")
            lev2.to_csv(apath)
        

if __name__=="__main__":
#     load_proxies()
#     load_all_data(skip_lever = False ,skip_price = False)
#     ids=["603259.sh","000661.sz"]
#     ids = get_stocks()

#     clean(ids)
    ids = None
    load_all_data(skip_lever = True ,skip_price = False,ids=ids)
#     load_all_data(skip_lever = True ,skip_price = False,ids=ids)
#     train_all(ids=ids)
#     filter_stk()
#      
#     
#     ct.test_all()
    
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
