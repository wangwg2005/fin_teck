# -*- coding: utf-8 -*-
import requests
import pandas as pd


def get_kline_day(sid):
    
    sid = convert_id(sid)

    url=f'https://img1.money.126.net/data/hs/kline/day/history/2021/{sid}.json'
    print(url)
    
    res = requests.get(url).json()
    sdata = res['data']
    df = pd.DataFrame(sdata, columns=['day','open','close','high','low','volume','increament'])
    
    return df
    
    
    
def convert_id(sid):
    """    """
    
    sid=sid[:6]
    if sid[0]>'4':
        return '0'+sid
    else:
        return '1'+sid
    