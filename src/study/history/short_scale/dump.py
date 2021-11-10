# -*- coding: utf-8 -*-

from study.realtime import inquery 
import pandas as pd
import matplotlib.pyplot as plt
import json

scale=1023
sid="sh000905"
data = inquery.split_time_window(sid, scale)

df=pd.DataFrame(data,dtype=float)

df.index=pd.to_datetime(df["day"])
df.pop("day")
fname=(sid+"_"+str(scale)+"_"+str(df.index[-1])+".json").replace(" ", "_").replace(":", "_")

with open(fname, "w") as f:
    json.dump(data, f)

df["close"].plot()
