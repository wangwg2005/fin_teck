# -*- coding: utf-8 -*-
import os
import pandas as pd
import math

sids_cache = None

def get_sids():
    
    if sids_cache is not None:
        return sids_cache
    
    sids = os.listdir("stock")
    sids = list(filter(lambda sid :sid<'010' or (sid>'600' and sid<'680'),sids))
    sids_cache = sids
    return sids

def model_pirce_volume(sid):
    df = pd.read_csv(os.path.join("stock",sid,"price.csv"),index_col=0,parse_dates=True)
    df = df[-2:].pct_change()
    return df.iloc[-1]
    
    
    
    
if __name__ == "__main__":
    pvr = model_pirce_volume("000850")
    print(pvr)