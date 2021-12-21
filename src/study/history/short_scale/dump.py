# -*- coding: utf-8 -*-

from study.realtime import inquery
import pandas as pd
import json
import os
import numpy as np


def dump_data(sid,scale=1023):
#     sid="sh000905"
    data = inquery.split_time_window(sid, datalen=scale)
#     print(data)
    df=pd.DataFrame(data)
    
    
    df.index=pd.to_datetime(df.pop("day"))
    df= df.astype({"open":float,"high":float,"low":float,"close":float,"volume":np.int64})
    
    fname=os.path.join("data",(sid+"_"+str(scale)+"_"+str(df.index[-1])+".json").replace(" ", "_").replace(":", "_"))
    
    
    with open(fname, "w") as f:
        json.dump(data, f)
        
    bl=os.path.join("data",sid+"_baseline.json")
    
    if not os.path.exists(bl):
        with open(bl, "w") as f:
            json.dump(data, f)
        
        
    return df
#     df["close"].plot()
    
if __name__=="__main__":
#     dump_data("sh000905")
    print(dump_data("sz000967"))
