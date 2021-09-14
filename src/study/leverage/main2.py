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


ttoday=datetime.date.today()

pre_day=tutil.get_prevous_trade_date(ttoday)

pre2_day=tutil.get_prevous_trade_date(pre_day)

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
    incr[:20].to_csv('..\\cache\\'+str(ttoday)+'_incr.csv')
    ratio[:20].to_csv('..\\cache\\'+str(ttoday)+'_ratio.csv')

    figure,ax=plt.subplots(2,1)
    figure.suptitle(pre_day)
    
    incr[:20].plot(x="证券简称",y="incr",kind="bar",rot="30",ax=ax[0])
    ratio[:20].plot(x="证券简称",y="quant",kind="bar",rot="30",ax=ax[1],stacked=True)

    plt.show()


def dump(year="2020"):
    fname=year+"_extreme_value.json"
    if os.path.exists(fname):
        return
    else:
        print("dummping price data")
    bds=bd.get_business_day_cn(year)
    days=pd.date_range(start=year+"-01-01",end=year+"-12-31",freq=bds)
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

def retrive_price_data(kv,duration):

    bds=bd.get_business_day_cn("2020")
    result={}
    for k in list(kv.keys())[:-7]:
#         if pre_k>k:
#             print(pre_k,k," disorder")
#             return
        
        sid=kv[k]
        fpath=os.path.join("cache",sid[:6]+".csv")
        
        if os.path.exists(fpath):
            df=pd.read_csv(fpath,index_col="Date",parse_dates=True)
        else:
            print("downloading",sid)
            df=yf.download(sid,start="2020-01-01",end="2021-01-01")
            if len(df)==0:
                print("no data fetched, stopping")
                break
            df.to_csv(fpath)

        term=pd.date_range(start=k,periods=duration,freq=bds)
        start_d=term[1]
        cprice=df.at[start_d,"Close"]
        df_s=df[term[0]:term[-1]]/cprice
        result[k]=df_s
        result[k+'pre']=df[:term[0]][-1:]
    
    return result


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

def top_profit():
    with open("2020_extreme_value.json","r") as f:
        top_sec=json.load(f)
    
    bds=bd.get_business_day_cn("2020")
    duration=20
#     term=pd.date_range(end='2020-12-31',periods=duration,freq=bds)
#     for i in term:
#         if i in top_sec:
#             del top_sec[i]
    
    prices=retrive_price_data(top_sec, duration)
    print(prices.keys())
    print(len(prices))
    
    
    dfs=[ df.reset_index() for df in prices.values() if len(df)==duration]

    y=[]
    y1=[]
    y2=[]
    for i in range(duration):
        prices_list=list(map(lambda a: a.at[i,'High'], dfs))
        y.append(sum(prices_list)/len(prices_list)-1)
        prices_list=list(map(lambda a: a.at[i,'Low'], dfs))
        y1.append(sum(prices_list)/len(prices_list)-1)
        prices_list=list(map(lambda a: a.at[i,'Close'], dfs))
        y2.append(sum(prices_list)/len(prices_list)-1)
        
    print(y)
    plt.plot(y)
    plt.plot(y1)
    plt.plot(y2)
    plt.show()
    

# dump()
top_profit()
# process()
