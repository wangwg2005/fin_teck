# -*- coding: utf-8 -*-
import datetime
from study.leverage import leverage_reader as lreader, downloader
import pandas as pd
import business_day
import time


ttoday=datetime.date.today()

def dump():
    days=pd.date_range(start="2021-06-21",end="2021-06-27",freq=business_day.get_business_day_cn("2021"))
#     print(days)
    days=map(lambda d:str(d)[:10],days)

    for day in days:
        print("downloading sse data for",day)
#         downloader.download_leverage_sse(day.replace("-",""))
        print("downloading szse data for",day)
        downloader.download_leverage_szse(day)
        time.sleep(3)
    
    
dump()