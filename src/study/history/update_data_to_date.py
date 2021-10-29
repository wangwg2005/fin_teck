# -*- coding: utf-8 -*-

from study.leverage import leverage_reader as lr
from datetime import date,timedelta
from study.history.update_index_prices import update_prices_to_date
from study.leverage import dump
import os


def update_leverage(date_str):
    lr.downloader.download_leverage_sse(date_str.replace("-",""))
    return lr.downloader.download_leverage_szse(date_str)
    
def update_leverage_2_date():
    day=date.today()
    up2date=True
    while up2date:
        day=day+timedelta(days=-1)
        day_str=day.strftime('%Y-%m-%d')
        up2date=update_leverage(day_str)
        print("update leverage date to",day_str)
    

def update_etf_lev():
    etfs={
#         "000016":{"sse":["510050"]},
#         "000905":{"szse":["159922"]}
        "000300":{"szse":["159919"],"sse":["510300","510310","510330"]}
#         "000905":{"sse":["510500","512500","510510","159922","szse":["159922"]]}

            
        }
    
    for code, item in etfs.items():
        for exchange, sids in item.items():
            print(sids)
            paths=list(map(lambda sid:os.path.join(code,sid+".xls"),sids))
            dump.extract_by_security(sids, exchange,"2020-01-01","2021-01-01",paths)
          
    
            
    
if __name__ =="__main__":
#     update_leverage_2_date()
    update_etf_lev()
#     update_prices_to_date()
#     update_index_lev(today_str)