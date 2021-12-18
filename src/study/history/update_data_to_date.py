# -*- coding: utf-8 -*-

from study.leverage import leverage_reader as lr
from datetime import date,timedelta
from study.history.update_index_prices import update_prices_to_date
from study.leverage import dump
import os
import pandas as pd
import business_day


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
#         "000905":{"szse":["159922"]}
#         "000300":{"szse":["159919"],"sse":["510300","510310","510330","515380"]}
        "000905":{"sse":["510500","512500","510510"],"szse":["159922"]}

            
        }
    
    for code, item in etfs.items():
        for exchange, sids in item.items():
            print(sids)
            paths=list(map(lambda sid:os.path.join(code,"rzrq_"+sid+".csv"),sids))
#             dump.extract_by_security(sids, exchange,"2020-01-01","2021-01-01",paths)
            dump.extract_fast(sids, exchange, paths)


def update_index_lev():
    today_str = (date.today()+timedelta(days=-1)).strftime("%Y-%m-%d")
    days = pd.date_range(start="2021-10-28",end=today_str,freq=business_day.get_business_day_cn("all"))
    # days = map(lambda day:day.strftime("%Y-%m-%d"),days)
    for name in ["000905"]:
        lev_fname = os.path.join(name, "融资融券_"+name+".xls")
        his_df = pd.read_excel(lev_fname, header=1, parse_dates=[0], index_col=0)
        data = list(map(lambda day: dump.extract_index_lev(name, day), days))
        his_df = his_df.append(data).sort_index()
        n_lev_fname = os.path.join(name, "融资融券_" + name + "n.xls")
        his_df.to_excel(n_lev_fname)
        print("update",name ," leverage to",days[-1])



def update_index():
#     update_leverage_2_date()
    update_etf_lev()
#     update_prices_to_date()
#     update_index_lev()



    
if __name__ =="__main__":
    update_index()
