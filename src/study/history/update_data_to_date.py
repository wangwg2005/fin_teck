# -*- coding: utf-8 -*-

from study.leverage import leverage_reader as lr
from datetime import date,timedelta
from study.history.update_index_prices import update_prices_to_date
from study.leverage import dump
import os
import pandas as pd
import business_day

abs_file = __file__
abs_dir = abs_file[:abs_file.rfind(os.path.sep)]


def update_leverage(date_str):
    lr.downloader.download_leverage_sse(date_str.replace("-",""))
    return lr.downloader.download_leverage_szse(date_str)
    
def update_leverage_2_date():
    day=str(date.today())[:10]
    up2date=True
    while up2date:
        days=pd.date_range(end=day,periods=2,freq=business_day.get_business_day_cn("all"))
        day = days[0] if day in days else days[1]
        print(days)
        print(day)
        day_str=day.strftime('%Y-%m-%d')
        up2date=update_leverage(day_str)
        print("update leverage date to",day_str)
    

def update_etf_lev():
    etfs={
#         "000016":{"sse":["510050"]},
#         "000905":{"szse":["159922"]},
#         "000300":{"szse":["159919"],"sse":["510300","510310","510330","515380"]},
#         "000905":{"sse":["510500","512500","510510"],"szse":["159922"]},
#         "000688":{"sse":["588000","588080"]},
#         "399006":{"szse":["159915"]}

            
        }
    
    for code, item in etfs.items():
        for exchange, sids in item.items():
            print(sids)
            paths=list(map(lambda sid:os.path.join(code,"rzrq_"+sid+".csv"),sids))
#             dump.extract_by_security(sids, exchange,"2020-01-01","2021-01-01",paths)
            dump.extract_fast(sids, exchange, paths)


def update_index_lev():
    today_str = (date.today()+timedelta(days=-1)).strftime("%Y-%m-%d")
#     today_str = '2022-03-10'
    days = pd.date_range(start="2022-05-26",end=today_str,freq=business_day.get_business_day_cn("all"))
#     days = pd.date_range(start="2020-01-02",end=today_str,freq=business_day.get_business_day_cn("all"))
    # days = map(lambda day:day.strftime("%Y-%m-%d"),days)
    for name in ["000016","000905","000300","000688"]:
#     for name in ["000688"]:
#     for name in ['000016']:
        lev_fname = os.path.join(abs_dir,name, "融资融券_"+name+".xls")
        his_df = pd.read_excel(lev_fname, header=1, parse_dates=[0], index_col=0)
        if len(days)>1:
            data = list(map(lambda day: dump.extract_index_lev(name, day), days))
            his_df = his_df.append(data).sort_index()
        n_lev_fname = os.path.join(abs_dir,name, "融资融券_" + name + "n.xls")
        his_df.to_excel(n_lev_fname)
        print("update",name ," leverage to",days[-1])



def update_index():
    update_leverage_2_date()
#     update_etf_lev()
    update_prices_to_date()
    update_index_lev()
    
def init_lev():
    root_dir = r'C:\Users\Darren\eclipse-workspace\fin_study\src\study\leverage'
    for exchange,c1name in zip(['sse','szse'],['标的证券代码','证券代码']):
        dir_path = os.path.join(root_dir,exchange)
        index_col= ['日期',c1name]
        df_all = []
        for file in os.listdir(dir_path):
            if file<'rzrqjygk2022':
                continue
            date_str = file[8:-4]
            df = pd.read_excel(os.path.join(dir_path,file),sheet_name=-1)
            df['日期']=date_str
            
            print(file)

            df=df.set_index(index_col)
            df_all.append(df)
                
            
            
        pd.concat(df_all).to_csv(exchange+'.csv',index_label=index_col )
        



    
if __name__ =="__main__":
    update_index()
#     init_lev()
