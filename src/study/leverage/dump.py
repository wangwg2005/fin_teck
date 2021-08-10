# -*- coding: utf-8 -*-
import datetime
from study.leverage import leverage_reader as lreader, downloader
import pandas as pd
import business_day
import time
import os
import numpy as np
import matplotlib.pyplot as plt


ttoday=datetime.date.today()


column_names=["融资买入额(元)","融资余额(元)","融券卖出量(股/份)","融券余量(股/份)","融券余额(元)","融资融券余额(元)"]

def dump():
    days=pd.date_range(start="2020-09-02",end="2020-12-31",freq=business_day.get_business_day_cn("2020"))
#     print(days)
    days=map(lambda d:str(d)[:10],days)

    for day in days:
        print("downloading sse data for",day)
        downloader.download_leverage_sse(day.replace("-",""))
        print("downloading szse data for",day)
        downloader.download_leverage_szse(day)
        time.sleep(3)
    

def summary_sse():
    
    index=[]
        
    data=None
    
    dir_path="sse"
    for file in os.listdir(dir_path):
        
        
        if "rzrqjygk2020" not in file :
            continue
        
        print(file)
        index.append(file[8:-4])
        
        df=pd.read_excel(os.path.join(dir_path,file))
        
        a=df[:1].to_numpy()
        
        if data is None:
            data=a
        else:
            data=np.append(data,a,axis=0)
    
    cnames=list(map(lambda s : s[2:], df.columns))

    output=pd.DataFrame(data=data,index=index,columns=cnames)
    
    output.to_excel("sse2020.xls")
    
def summary_szse():
        
    index=[]
        
    data=None
    
    dir_path="szse"
    for file in os.listdir(dir_path):
        
        
        if "rzrqjygk2020" not in file :
            continue
        
        print(file)
        index.append(file[8:-4])
        
        df=pd.read_excel(os.path.join(dir_path,file))
        b=df[df.columns[2:]].applymap(lambda x:int(x.replace(",","")))
        a=b.sum().to_numpy().reshape([1,6])
        
        if data is None:
            data=a
        else:
            data=np.append(data,a,axis=0)

    
    output=pd.DataFrame(data=data,index=index,columns=column_names)
    
    output.to_excel("szse2020.xls")
    
def summary():
    sse=pd.read_excel("sse2020.xls", index_col=0,parse_dates=True)
    szse=pd.read_excel("szse2020.xls", index_col=0,parse_dates=True)
    
    summ=sse.copy()
    
    for col in column_names:
        summ[col]=summ[col]+szse[col]

    summ.to_excel("2020_total.xls")
    
    
def extract(security_codes,exchange,prefix="2020"):
    pref="rzrqjygk"+prefix
    
    kv={}
    index=[]
    for file in os.listdir(exchange):
        if pref not in file :
            continue
        index.append(file[8:-4])
        df=pd.read_excel(os.path.join(exchange,file),sheet_name=-1,dtype={"标的证券代码":str})
        for code in security_codes:
            row=df[df[df.columns[0]]==code][df.columns[2:]][:1].to_numpy()
            if code not in kv:
                kv[code]=row
            else:
                kv[code]=np.append(kv[code],row,axis=0)
    for code in security_codes:
        df=pd.DataFrame(kv[code],columns=column_names,index=index).applymap(lambda x:int(x.replace(",","")))
        fname=code+"_2020.xls"
        print("saving",fname)
        df.to_excel(fname)
        
if __name__ == '__main__':
    
#     summary()
    parent_dir=os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    csi500=pd.read_csv(os.path.join(parent_dir,"history","csi500","000905.csv"),index_col="日期",encoding="gbk",parse_dates=True)
    print(csi500["2020-01-01":"2020-12-31"]["收盘价"])
       
    kv={}
    targ_dir="study"
    for file in os.listdir(targ_dir):
        kv[file[:-4]]=pd.read_excel(os.path.join(targ_dir,file),index_col=0,parse_dates=True)
       
    total=kv.pop("2020_total")
       
    print("tag1-------------")
    print(total[column_names[1]]) 
       
    for k,v in kv.items():
        total[column_names[1]]-=v[column_names[1]]
          
          
    print("tag2-------------")
    print(total[column_names[1]])
           
    total["risk"]=(2.7*csi500["收盘价"]-1000-total[column_names[1]]/100000000)*2
    total["risk"].plot()
    plt.show()
    
    
    
    
#     extract(["510900","518880"],"sse")     
#     extract(["518880"],"sse")
#     extract(["159920","159934"],"szse")