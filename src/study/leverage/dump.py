# -*- coding: utf-8 -*-
import datetime
from study.leverage import  downloader
import pandas as pd
import business_day
import time
import os
import numpy as np


ttoday=datetime.date.today()
base_path=os.path.split(os.path.realpath(__file__))[0]

column_names=["融资买入额(元)","融资余额(元)","融券卖出量(股/份)","融券余量(股/份)","融券余额(元)","融资融券余额(元)"]

def dump():
    days=pd.date_range(start="2021-09-22",end="2021-10-21",freq=business_day.get_business_day_cn("2021"))
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
    
    if exchange=="sse":
        sid_cname='标的证券代码'
    else:
        sid_cname="证券代码"
    
    kv={}
    index=[]
    for file in os.listdir(exchange):
        if pref not in file :
            continue
        index.append(file[8:-4])
        df=pd.read_excel(os.path.join(exchange,file),sheet_name=-1,dtype={sid_cname:str})
        
        for code in security_codes:
            row=df[df[sid_cname]==code][df.columns[2:]][:1].to_numpy()
            if code not in kv:
                kv[code]=row
            else:
                kv[code]=np.append(kv[code],row,axis=0)
    print(df.columns)
    for code in security_codes:
        data=kv[code]
        if len(data)==0 :
            print("no data for",code)
            continue
        elif len(data)!=len(index):
            print("data length dosn't match index length:",code)
            continue
        df=pd.DataFrame(data,columns=column_names,index=index).applymap(lambda x: x if type(x)==int else int(x.replace(",","")))
        fname=os.path.join("cache",code+"_"+prefix+".xls")
        print("saving",fname)
        df.to_excel(fname)
        
        
def extract4cache():
    sse_stock=[]
    szse_stock=[]
    for file in os.listdir("cache"):
        if len(file)>10:
            continue
        if file[0]=='6':
            sse_stock.append(file[:6])
        else:
            szse_stock.append(file[:6])
    extract(sse_stock, "sse")
    extract(szse_stock, "szse")
    
    
def extract_fast(security_codes,exchange,paths):
    prefix='rzrqjygk'
    
    if exchange=="sse":
        date_format = prefix + '%Y%m%d.xls'
        cnames = ['标的证券代码', "本日融资余额(元)"]
        nnames = {"标的证券代码": "sid", "本日融资余额(元)": "lev"}
    else:
        date_format= prefix + '%Y-%m-%d.xls'
        cnames=["证券代码","融资余额(元)"]
        names={"证券代码":"sid","融资余额(元)":"lev"}
    
    has_empty=len(list(filter(lambda path:not os.path.exists(path),paths)))>0

    last_days={}
    
    if has_empty:
        mode="w"
        files=os.listdir(os.path.join(base_path,exchange))
        print("scan all leverage files")
    
    else:
        mode="a"
        dfs=map(lambda path: pd.read_csv(path), paths)
        last_days=list(map(lambda df: str(df.iat[-1,0]), dfs))
        last_day=min(last_days)
        print("scan leverage file from",last_day)
        last_days=dict(zip(security_codes,map(lambda d: prefix+str(d)[:10]+".xls",last_days)))
#         last_day = pref + last_day
#         files=filter(lambda day: day>last_day, files)
        
    
        days=pd.date_range(start=last_day,end=datetime.date.today(),freq=business_day.get_business_day_cn())[1:]
        if str(datetime.date.today())[:10] in days:
            days=days[:-1]
        if len(days)==0:
            return 
        files=map(lambda day:day.strftime(date_format),days)
        
    
        
    sid_cname=cnames[0]
    kv={ code: {"index":[]} for code in security_codes}
    files=list(files) 
    print(files)
    for file in files:
        index=file[8:-4]
        if len(index)==8:
            index=index[:4]+"-"+index[4:6]+"-"+index[6:]
        fpath=os.path.join(base_path,exchange,file)
        # print(fpath)
        df=pd.read_excel(fpath,sheet_name=-1,dtype={sid_cname:str})
        for code in security_codes:
            
            if code in last_days and last_days[code]>=file:
                    continue
            
            row=df[df[sid_cname]==code][df.columns[2:]][:1].to_numpy()
            if len(row)==0:
                continue
            kv[code]["index"].append(index)
            
            if "data" not in kv[code]:
                kv[code]["data"]=row
            else:
                kv[code]["data"]=np.append(kv[code]["data"],row,axis=0)
    cnames = map(lambda a : a.replace("本日", ""), df.columns[2:])
    cnames=list(map(lambda a:a.replace("(股/份)", ""), cnames))
#     cnames.insert(0, "日期")
#     dfs=[]
    for i in range(len(security_codes)):
        code=security_codes[i]
        if "data" not in kv[code]:
            continue
        
        data=kv[code]["data"]
        if len(data)==0 :
            print("no data for",code)
            continue
#         elif len(data)!=len(index):
#             print("data length dosn't match index length:",code)
#             continue
#         print(kv[code]["index"])
#         print(data)
        ndf=pd.DataFrame(data,columns=cnames,index=kv[code]["index"]).applymap(lambda x: x if type(x)==int else int(x.replace(",","")))
        ndf.index.name="日期"
#         ndf=ndf[:-1]
        s = ndf.to_csv(None,header=has_empty)
        with open(paths[i],mode,encoding="utf8", newline='') as f:
            f.write(s)
        print(code,"is updated to",ndf.index[-1])


    
def extract_by_security(security_codes,exchange,start_date,end_date,paths):
    days=pd.date_range(start=start_date,end=end_date,freq=business_day.get_business_day_cn("all"))
    

    
    if exchange=="sse":
        days = map(lambda d:d.strftime('%Y%m%d'),days)
        cnames = ['标的证券代码', "本日融资余额(元)"]
        nnames = {"标的证券代码": "sid", "本日融资余额(元)": "lev"}
    else:
        days=map(lambda d:d.strftime('%Y-%m-%d'),days)        
        cnames=["证券代码","融资余额(元)"]
        names={"证券代码":"sid","融资余额(元)":"lev"}
        
        
    pref="rzrqjygk"
        
    sid_cname=cnames[0]
    kv={ code: {"index":[]} for code in security_codes}
    

    for file in os.listdir(os.path.join(base_path,exchange)):
        if pref not in file :
            continue
        index=file[8:-4]
        fpath=os.path.join(base_path,exchange,file)
        # print(fpath)
        df=pd.read_excel(fpath,sheet_name=-1,dtype={sid_cname:str})
        for code in security_codes:
            
            row=df[df[sid_cname]==code][df.columns[2:]][:1].to_numpy()
            if len(row)==0:
                continue
            kv[code]["index"].append(index)
#             print(index,":",row)
            if "data" not in kv[code]:
                kv[code]["data"]=row
            else:
                kv[code]["data"]=np.append(kv[code]["data"],row,axis=0)
    cnames = map(lambda a : a.replace("本日", ""), df.columns[2:])
    cnames=list(map(lambda a:a.replace("(股/份)", ""), cnames))
#     dfs=[]
    for i in range(len(security_codes)):
        code=security_codes[i]
        data=kv[code]["data"]
        if len(data)==0 :
            print("no data for",code)
            continue
#         elif len(data)!=len(index):
#             print("data length dosn't match index length:",code)
#             continue
#         print(kv[code]["index"])
#         print(data)
        ndf=pd.DataFrame(data,columns=cnames,index=kv[code]["index"]).applymap(lambda x: x if type(x)==int else int(x.replace(",","")))
        ndf.index.name="日期"
        if paths is None:
            fname=os.path.join("cache",code+"_"+start_date+"_"+end_date+".xls")
        else:
            fname=paths[i]
        print("saving",fname)
        ndf.to_excel(fname)
        print(fname,"saved")
#         dfs.append(ndf)
        
#     return dfs
    
    
    
    
def extract_index_lev(ind_code,date_val):
    date_str=date_val.strftime("%Y-%m-%d")
    prefix="rzrqjygk"
    df=pd.read_excel(os.path.join(base_path,"index_composite",ind_code+"closeweight.xls"),dtype={"成分券代码Constituent Code":str})
    # print(df["成分券代码Constituent Code"])
    szse = df[df['交易所Exchange'] == "深圳证券交易所_股票"]
    sse = df[df['交易所Exchange'] == "上海证券交易所_股票"]
    
    fname = os.path.join(base_path,"sse",prefix+date_str.replace("-", "")+".xls")
    sse_df= pd.read_excel(fname,sheet_name=-1,dtype={'标的证券代码':str})
    ids=list(sse["成分券代码Constituent Code"])
    sec_sse=sse_df[sse_df["标的证券代码"].isin(ids)]
    sum_sse=sec_sse[["本日融资余额(元)","本日融券余量"]].sum().to_numpy()
    # print("sum sse",sum_sse)
    
    fname = os.path.join(base_path, "szse", prefix+date_str+".xls")
    szse_df = pd.read_excel(fname,sheet_name=-1, dtype={'证券代码': str})
    ids = list(szse["成分券代码Constituent Code"])
    sec_szse = szse_df[szse_df["证券代码"].isin(ids)]
    sum_szse = sec_szse[["融资余额(元)", "融券余量(股/份)"]].applymap(lambda a: int(a.replace(",", ""))).sum().to_numpy()
    # print("sum szse", sum_szse)
    
    sumup = (sum_sse+sum_szse)/100000000
    return pd.Series({"融资余额(亿元)":sumup[0],"融券余量(亿股)": sumup[1]},name=date_val)
    
    
    
if __name__ == '__main__':
    
#     dump()

    # extract_by_security(["510510"], "sse","2020-01-01","2020-12-31",None)

    path=r'C:\Users\Darren\eclipse-workspace\fin_study\src\study\history\stock\000723\leverage.csv'
    extract_fast(["000723"], "szse", [path])
#     print(extract_index_lev("000905","2021-10-27"))

#     summary()
#     parent_dir=os.path.abspath(os.path.join(os.getcwd(), os.pardir))
#     csi500=pd.read_csv(os.path.join(parent_dir,"history","csi500","000905.csv"),index_col="日期",encoding="gbk",parse_dates=True)
#     print(csi500["2020-01-01":"2020-12-31"]["收盘价"])
#        
#     kv={}
#     targ_dir="study"
#     for file in os.listdir(targ_dir):
#         kv[file[:-4]]=pd.read_excel(os.path.join(targ_dir,file),index_col=0,parse_dates=True)
#        
#     total=kv.pop("2020_total")
#        
#     print("tag1-------------")
#     print(total[column_names[1]]) 
#        
#     for k,v in kv.items():
#         total[column_names[1]]-=v[column_names[1]]
#           
#           
#     print("tag2-------------")
#     print(total[column_names[1]])
#            
#     total["risk"]=(2.7*csi500["收盘价"]-1000-total[column_names[1]]/100000000)*2
#     total["risk"].plot()
#     plt.show()
    
    
    
    
#     extract(["510900","518880"],"sse")     
#     extract(["600375"],"sse")
#     extract(["159920","159934"],"szse")