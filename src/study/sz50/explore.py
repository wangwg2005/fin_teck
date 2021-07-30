# -*- coding: utf-8 -*-

#explore the futures impact

import pandas as pd
from pandas.tseries.offsets import DateOffset

dates=pd.date_range('2019-01-01','2021-07-30',freq='WOM-3FRI')

print(dates)

df=pd.read_csv(r"000016.csv",index_col="日期",parse_dates=["日期"],encoding='gbk')


df["diff"]=df['收盘价'].rolling(window=8).max()-df['收盘价']
df["incr"]=df["diff"]/df['收盘价']


dd=list(dates)

a=df[df.index.isin(dates)]

print(a[["收盘价","涨跌幅","diff","incr"]])
