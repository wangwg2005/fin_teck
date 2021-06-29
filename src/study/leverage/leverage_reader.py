# -*- coding: utf-8 -*-

import pandas as pd
import os
from study.leverage import downloader

def read_detail_sse(date_str):
    fpath=os.path.join("sse","rzrqjygk"+date_str+".xls")
    
    if not os.path.exists(fpath):
        print("downloading file for",date_str)
        downloader.download_leverage_sse(date_str)
    
    df=pd.read_excel(fpath,sheet_name="明细信息")
    
    return df
    
# read_detail_sse("20210621")