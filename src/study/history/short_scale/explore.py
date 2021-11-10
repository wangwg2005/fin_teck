# -*- coding: utf-8 -*-

import pandas as pd
import mplfinance as mpf
from study.quant import datasource as ds

df=pd.read_json("sh000905_1023_2021-11-10_15_00_00.json")
df.index=pd.to_datetime(df.pop("day"))

print(df.columns)

delta=df["close"]-df["open"]
delta=delta.map(lambda a: 1 if a>0 else -1)
vol1=df["volume"]*delta
df["vol1"]=vol1.cumsum()
leng=48*20

df=df[-leng:]

print(df)

add_plot=[mpf.make_addplot(df['vol1']),mpf.make_addplot(df['ma_price20'],linestyle='dashdot')]


mpf.plot(df,type="candle",style=ds.get_style(),addplot=add_plot)