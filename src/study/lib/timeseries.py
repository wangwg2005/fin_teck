# -*- coding: utf-8 -*-

import pandas as pd

def gen_timeseries(year,days=365):
    days2019=[]
    y2019=pd.date_range(year+"-01-01",periods=days,freq="D")
    for i in range(days):
        dateStr=y2019[i].strftime("%Y-%m-%d")
        item={"id":i,"date":dateStr}
        days2019.append(item)
    return days2019

print(gen_timeseries("2019"))