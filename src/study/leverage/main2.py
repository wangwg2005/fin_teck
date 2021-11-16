# -*- coding: utf-8 -*-
import datetime
from study.leverage import time_util as tutil
from study.leverage import leverage_reader as lreader
import pandas as pd
import matplotlib.pyplot as plt
import business_day as bd
import yfinance as yf
import json
import os
from math import ceil
import mplfinance as mpf
import numpy as np
from study.realtime import price_query
import file_cache as fc
import business_day as bd
import seaborn as sns



ttoday=datetime.date.today()
today_str=str(ttoday)


bdays=pd.date_range(end=datetime.date.today(),periods=3,freq=bd.get_business_day_cn("all"))[:2]

pre2_day,pre_day=bdays


ind=0
dump_path="top"+str(ind)+".json"

def filter_sse():

    pre_day_str=tutil.stringfy(pre_day)
    df1=lreader.read_detail_sse(pre_day_str)
    
    pre2_day_str=tutil.stringfy(pre2_day)
    df2=lreader.read_detail_sse(pre2_day_str)
    
    
    df=df1[["标的证券简称"]]
    df=df.rename(columns={"标的证券简称":"证券简称"})
    df[pre_day_str]=df1["本日融资余额(元)"]
    df[pre2_day_str]=df2["本日融资余额(元)"]
    
    df=df.filter(regex="^60", axis=0)
    df["incr"]=df[pre_day_str]/df[pre2_day_str]-1
    df["quant"]=df[pre_day_str]-df[pre2_day_str]
    
    dfn=df.sort_values(by=['incr'],ascending=False)
    
#     print(dfn.head(20))
    
    dfn2=df.sort_values(by=['quant'],ascending=False)
    
#     print(dfn2.head(20))
#     dfn[:20].plot(x="证券简称",y="incr",kind="bar",rot="30")
#     dfn2[:20].plot(x="证券简称",y="incr",kind="bar",rot="30")
    
    return dfn[:20],dfn2[:20],dfn[-20:],dfn2[-20:]
    
    
def convert_number(a):
    return int(a.replace(",",""))
    
def filter_szse():
    pre_day_str=str(pre_day)[:10]
    df1=lreader.read_detail_szse(pre_day_str)
    
    pre2_day_str=str(pre2_day)[:10]
    df2=lreader.read_detail_szse(pre2_day_str)
    
    cname1=tutil.stringfy(pre_day)
    cname2=tutil.stringfy(pre2_day)
    
    df=df1[["证券简称"]]
    df[cname1]=df1["融资余额(元)"].map(convert_number)
    df[cname2]=df2["融资余额(元)"].map(convert_number)
    df=df.filter(like="00", axis=0)
    df["incr"]=df[cname1]/df[cname2]-1
    df["quant"]=df[cname1]-df[cname2]
    
    dfn=df.sort_values(by=['incr'],ascending=False)
#     dfn[:20].plot(x="证券简称",y="incr",kind="bar",rot="30")
#     print(dfn.head(20))
    
    dfn2=df.sort_values(by=['quant'],ascending=False)
#     dfn2[:20].plot(x="证券简称",y="incr",kind="bar",rot="30")
#     print(dfn2.head(20))
    
    return dfn[:20],dfn2[:20],dfn[-20:],dfn2[-20:]

def merge_ordered(df1,df2,columns,ascending=False):
    df=pd.concat([df1,df2])
    df=df.sort_values(by=columns,ascending=ascending)
    return df
    

def process(retn=False):
    sse1, sse2,sse3,sse4=filter_sse()
    szse1,szse2,szse3,szse4=filter_szse()
        # ax1=plt.figure(2,1,1)
    incr=merge_ordered(sse1, szse1, ['incr'])
    
#     incr[:20].plot(y="incr",kind="bar",rot="30",ax=ax[0])
    # ax2=plt.figure(2,1,2)
    ratio=merge_ordered(sse2,szse2,['quant'])
    
#     ratio[:20].plot(y="quant",kind="bar",rot="30",ax=ax[1],stacked=True)
#     if(retn):
        
#     abs_path=os.path.abspath("..")
#     print(abs_path)
    incr[:20].to_csv('..\\cache\\'+today_str+'_incr.csv')
    ratio[:20].to_csv('..\\cache\\'+today_str+'_ratio.csv')

    figure,ax=plt.subplots(2,1)
    figure.suptitle(pre_day)
    
    incr[:20].plot(x="证券简称",y="incr",kind="bar",rot="30",ax=ax[0])
    ratio[:20].plot(x="证券简称",y="quant",kind="bar",rot="30",ax=ax[1],stacked=True)

    plt.show()


def get_bussness_days_2019():
    res=price_query.get_history_price("sh000001", 800)
    days=[ a["day"] for a in res if "2019" in a["day"] ]
    
    return days

def get_bussness_days_recent(day_num):
    res=price_query.get_history_price("sh000001", day_num)
    days=[ a["day"] for a in res ]
    
    return days
    

def dump(year="2020"):
    fname=year+"_extreme_value.json"
    if os.path.exists(fname):
        return
    else:
        print("dummping price data")
    bds=bd.get_business_day_cn(year)
    days=pd.date_range(start=year+"-01-01",end=year+"-09-18",freq=bds)
#     days=get_bussness_days_recent(1023)
    print("trade days back from today",len(days))
    kv={}
    for i in range(1,len(days)):
        global pre_day, pre2_day
        pre_day=days[i]
        pre2_day=days[i-1]
        sse1, sse2, sse3, sse4=filter_sse()
        szse1, szse2,szse3,szse4=filter_szse()
        
        top_quant=merge_ordered(sse1, szse1, "quant")[:10]
        top_ratio=merge_ordered(sse2, szse2, "incr")[:10]
        buttom_quant=merge_ordered(sse3, szse3, "quant",ascending=True)[:10]
        buttom_ratio=merge_ordered(sse4, szse4, "incr",ascending=True)[:10]
         
        val={"quant_top":top_quant.index.to_list(),"quant_buttom":buttom_quant.index.to_list(),"ratio_top":top_ratio.index.to_list(),"ratio_buttom":buttom_ratio.index.to_list()}
        print(days[i],val)
        kv[str(pre_day)[:10]]=val
        
    #         ratio = pd.concat([sse2,szse2])
    with open(fname,"w",encoding="gbk") as ff:
        ff.write(json.dumps(kv))

def simulate(df,indexes ):
    stand_price=df.at[indexes[0],"Close"]
    f_price=df.at[indexes[1],"Low"]
    h_price=df.at[indexes[1],"High"]
    o_price=df.at[indexes[1],"Open"]
    buy_stand=stand_price*0.97
    if f_price>buy_stand:
        return 0,0,0
    buy_price=buy_stand if o_price>buy_stand else (f_price+o_price)/2
    
    quota=ceil(10000/(buy_price*100))
    sell_price=None
    for ind in indexes[2:]:
        h_price=df.at[ind,"High"]
        o_price=df.at[ind,"Open"]
        sell_stand=buy_price*1.03
        if h_price>sell_stand:
            sell_price=sell_stand if sell_stand<o_price else (o_price+h_price)/2
            break
    if sell_price is None:
        sell_price=df.at[ind,"Close"]
        
    profit=(sell_price-buy_price)*quota*100
    return profit,buy_price, sell_price

def normalize(price_open,*prices):
    
    return (1, *[p/price_open for p in prices])

def get_style():
    mc = mpf.make_marketcolors(
        up='red', 
        down='green', 
        edge='i', 
        wick='i', 
        volume='in', 
        inherit=True)
    
    style = mpf.make_mpf_style(base_mpl_style="ggplot", marketcolors=mc)
    return style

def filter_out(df_range,i_tems):
    cell_v=df_range.at[i_tems[1],'Low']
    return  cell_v<-0.8



def retrive_price_data(sid,start_date,duration):
    year=start_date[:4]
    next_year=str(int(year)+1)

    bds=bd.get_business_day_cn(year)
    term=pd.date_range(start=start_date,periods=duration,freq=bds)
#         if pre_k>k:
#             print(pre_k,k," disorder")
#             return
    if term[0].year==term[-1].year:
        
        fpath=os.path.join("cache",sid[:6]+"_"+year+".csv")
        
        if os.path.exists(fpath):
            df=pd.read_csv(fpath,index_col="Date",parse_dates=True)
        else:
            print("downloading",sid,"for date",start_date)
            df=yf.download(sid,start=year+"-01-01",end=next_year+"-01-01")
            df.to_csv(fpath)
            if len(df)==0:
                print("no data fetched, stopping")
                return
            
    
        
        start_d=term[0]
        if start_d not in df.index:
            return None
        cprice=df.at[start_d,"Close"]
        df_s=df[term[0]:term[-1]]/cprice
    else:
        
#         fpath=os.path.join("cache",sid[:6]+"_"+start_date+"_"+str(duration)+".csv")
#         
#         if os.path.exists(fpath):
#             df=pd.read_csv(fpath,index_col="Date",parse_dates=True)
#         else:
#             print("downloading",sid,"for date",start_date)
#             df=yf.download(sid,start=start_date,period=duration)
#             df.to_csv(fpath)
#             if len(df)==0:
#                 print("no data fetched, stopping")
#                 return
#             
#     
#         
#         start_d=term[0]
#         if start_d not in df.index:
#             return None
#         cprice=df.at[start_d,"Close"]
#         df_s=df[term[0]:term[-1]]/cprice
        
        df_s= None
    
    return df_s


def group_stock(df):
    pass


def avg_reach_10_days():
    dump()
    
    with open(dump_path,"r") as f:
        top_sec=json.load(f)
    
    prices=retrive_price_data(top_sec, 30)
    x=[]
    y=[]
    c=[]
    for k in list(top_sec.keys())[:-7]:
        df=prices[k]
        df=df.reset_index()
#         print(df)
        result=df[df['High']>1.10]
        if len(result)>0:
            y.append(result.index[0])
        else:
            y.append(-1)
            
        x.append(k)
    
    
    print('x',x)
    print('y',y)
    
    print('total trade number',len(y))
    print('number of -1 :',y.count(-1))
    above_0=list(filter(lambda a: a>0,y))
    avg_number=sum(above_0)/len(above_0)
    print('avg 10% day',avg_number)
    plt.scatter(x,y)
    plt.show()
    
    
def get_range(date_str,duration,sid,day_number):
    
    
    
    cache_fname=sid[:6]+"_sina.json"
    
    arr=fc.json_cache(cache_fname, price_query.get_history_price, price_query.convert_sid(sid), day_number)
    for i in range(len(arr)):
        if arr[i]["day"]>=date_str:
            break;
    
    return arr[i:i+duration]
    
    
    
def get_price_from_sina(items,duration):
    size=len(items)
    print("stock number:",size)
    day_number=size
    days=fc.json_cache("trade_days.json", get_bussness_days_recent, 2013)
    for date_str,v in items:
        sids=list(map(lambda a:a[0],v.values()))
        print(sids)
        prices=list(map(lambda sid:get_range(date_str,duration,sid,day_number),sids))
        print("key date",date_str)
        print("prices for",sids)
        print(prices)
        day_number-=1
            
            
def classification(mname):
    year="2020"
    duration=60
#     model1=None
    model_path="model1_{0}_{1}.json".format(60,year)
    with open(model_path,"r",encoding="utf8") as f:
        model1=json.load(f)
        
    with open(year+"_extreme_value.json","r") as f:
        top_sec=json.load(f)
    
    col_name='quant_buttom'
    dfs=map(lambda item:retrive_price_data(item[1][col_name][0],item[0],duration),top_sec.items())
  

#     
    dfs=[ df.reset_index() for df in dfs if df is not None and len(df)==duration]
    cols=['quant_buttom','quant_top','ratio_top','ratio_buttom']
    
    for col_name in cols:
        for pos in range(10):
        
            high_map=map(lambda df:(df.at[pos,"High"],df.at[duration-1,"High"]),dfs)
        #     above_high=list(filter(lambda h:h[0]-1>model1["model"][col_name]["high"][pos]["mean"],high_map))
            a1=list(zip(*high_map))
            print(list(a1))
            ax=plt.subplot(211)
            sns.regplot(x=np.array(a1[0]), y=np.array(a1[1]),ax=ax)
#             ax.scatter(a1[0],a1[1])
#             x=np.linspace(0.9,1.1,100)
#             ax.plot(x,x,color='red')
            ax.set_title(col_name+"_high_"+str(pos)+".png")
            
            
            
            low_map=list(map(lambda df:(df.at[pos,"Low"],df.at[duration-1,"Low"]),dfs))
            print("low map",low_map)
            print("low pos",model1["model"][col_name]["low"][pos]["mean"])
            print(model1)
        
        #     below_high=list(filter(lambda h:h[0]-1<=model1["model"][col_name]["low"][pos]["mean"],low_map))
            
        #     
            
            a2=list(zip(*low_map))
            print(a2)
            ax=plt.subplot(212)
            sns.regplot(x=np.array(a2[0]), y=np.array(a2[1]),robust=True,ax=ax)
            ax.set_title(col_name+"_low_"+str(pos)+".png")
            
#             plt.savefig("img//explore_"+col_name+"_"+str(pos)+"_robust.png")
            plt.close()
    
    
        
        

def top_profit_summary(year="2020",force=False):
    duration=30
    model1={}
    model_path="model1_{0}_{1}.json".format(duration,year)
    print(model_path)
    if not force and os.path.exists(model_path):
        with open(model_path,"r",encoding="utf8") as f:
            model1=json.load(f)
        model=model1["model"]
    else:
        model1={"properties":{"version":0.01,"name":"top profit","params":{"duration":duration,"year":year},"timestamp":str(datetime.date.today())}}
        model={}
        model1["model"]=model
        with open(year+"_extreme_value.json","r") as f:
            top_sec=json.load(f)
            
        
        
        
    #             del top_sec[i]
#         get_price_from_sina(top_sec.items(),duration)
        cols=['quant_buttom','quant_top','ratio_top','ratio_buttom']
        detail={}
        for ind in range(len(cols)):
            col_name=cols[ind]
            
            fname=col_name+".csv"
            if os.path.exists(fname):
                df_all=pd.read_csv(fname,index_col=[0])
                dfs=[df_all.loc[k] for k in top_sec.keys() if k in df_all.index]
            else:
            
                dfs=map(lambda item:retrive_price_data(item[1][col_name][0],item[0],duration),top_sec.items())
                df_all=pd.concat(dfs,keys=top_sec.keys())
                df_all.to_csv(fname)
              
  
        #     
            dfs=[ df.reset_index() for df in dfs if df is not None and len(df)==duration]
          
            highs=[]
            lows=[]
            closes=[]
              
            detail[col_name]={"high":[],"low":[],"close":[]}
              
            for i in range(duration):
                prices_list=list(map(lambda a: a.at[i,'High'], dfs))
                detail[col_name]["high"].append(prices_list)
        #         if
                var_val={"mean":np.mean(prices_list)-1,"median": np.median(prices_list)-1,"std": np.std(prices_list)}
                highs.append(var_val)
                  
                prices_list=list(map(lambda a: a.at[i,'Low'], dfs))
                detail[col_name]["low"].append(prices_list)
#                 detail["low"]=prices_list
                lows_val={"mean":np.mean(prices_list)-1,"median": np.median(prices_list)-1,"std": np.std(prices_list)}
                lows.append(lows_val)  
                  
                prices_list=list(map(lambda a: a.at[i,'Close'], dfs))
                detail[col_name]["close"].append(prices_list)
                close_val={"mean":np.mean(prices_list)-1,"median": np.median(prices_list)-1,"std": np.std(prices_list)}
                closes.append(close_val)
                  
            model[col_name]={"high":highs,"low":lows,"close":closes}
    #     print(y)
        with open(model_path,"w",encoding="utf8") as f:
            print(model1)
            json.dump(model1, f)
              
        with open("detail_{0}.json".format(year),"w") as f:
            json.dump(detail,f)
             
    keys=list(model.keys())
     
    for col in ["mean","median","std"]:
     
        for ind in range(len(model)):
            ax=plt.subplot(2,2,ind+1)
            key=keys[ind]
            ax.set_title(key)
            ax.plot(list(map(lambda a:a[col],model[key]["high"])))
            ax.plot(list(map(lambda a:a[col],model[key]["low"])))
            ax.plot(list(map(lambda a:a[col],model[key]["close"])))
            title="model_{0}_{1}_{2}.png".format(duration,col,year)
#         plt.figure(figsize=(13,7), dpi=100)
        plt.savefig(title)
        plt.show()
        plt.close()
    
#     plt.show()
    

# dump()
# top_profit()
if __name__=="__main__":
#     pass
#     today_str="2021-11-12"
    process()
#     pass
#     dump("all")
#     top_profit_summary(year="2019_now",force=True)
#     classification("")
#     get_bussness_days()
