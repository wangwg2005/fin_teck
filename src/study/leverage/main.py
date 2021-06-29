# -*- coding: utf-8 -*-
import datetime
from study.leverage import time_util as tutil
from study.leverage import leverage_reader as lreader
import pandas as pd

ttoday=datetime.date.today()

pre_day=tutil.get_prevous_trade_date(ttoday)

pre2_day=tutil.get_prevous_trade_date(pre_day)

pre_day_str=tutil.stringfy(pre_day)
df1=lreader.read_detail_sse(pre_day_str)

pre2_day_str=tutil.stringfy(pre2_day)
df2=lreader.read_detail_sse(pre2_day_str)



def reindex(df):
    ind_ser=df.pop("标的证券代码")
    df.index=ind_ser 



reindex(df1)
reindex(df2)

df=df1[["标的证券简称"]]
df["day2"]=df1["本日融资余额(元)"]
df["day1"]=df2["本日融资余额(元)"]

df["incr"]=df["day2"]/df["day1"]-1

dfn=df.sort_values(by=['incr'],ascending=False)

print(dfn.head(20))

