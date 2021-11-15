# -*- coding: utf-8 -*-

from study.realtime import inquery
import pandas as pd
import matplotlib.pyplot as plt
import json

def dump_data(sid):
    scale=1023
#     sid="sh000905"
    data = inquery.split_time_window(sid, datalen=scale)
    print(data)
    df=pd.DataFrame(data,dtype=float)
    
    df.index=pd.to_datetime(df["day"])
    df.pop("day")
    fname=(sid+"_"+str(scale)+"_"+str(df.index[-1])+".json").replace(" ", "_").replace(":", "_")
    
    with open(fname, "w") as f:
        json.dump(data, f)
    
    df["close"].plot()
    
if __name__=="__main__":
#     dump_data("sh000905")
    dump_data("sh000300")
