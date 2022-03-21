# -*- coding: UTF-8 -*- 

import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import requests
from datetime import datetime
import tensorflow as tf
import numpy as np

def get_feature(sid):

    today_str = str(datetime.today())[:10]
    print("today str:",today_str)
    data_len = 1024
    r = requests.get(f'https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={sid},day,,{today_str},{data_len},qfq').json()
    
    print(r)
    df = pd.DataFrame.from_records(r['data'][sid]['qfqday'],columns=['day','open','close','high','low','volume'])
    df=df.set_index('day');
    
    df['close']=df['close'].astype(float)
    df['high']=df['high'].astype(float)
    df['volume']=df['volume'].astype(float)
    
    # df=df[:300]
    # df = pd.read_csv(r'C:\Users\Darren\eclipse-workspace\fin_study\src\study\history\stock\002118\price.csv',encoding='utf8',index_col=[0],parse_dates=True)[-500:];
    win = 5
    df['vol_price'] = df['close'].rolling(win).std(ddof=0)*10
    df['vol_volume'] = df['volume'].rolling(win).std(ddof=0)/100000/2
    df['max']=df['high'].rolling(win).max().shift(-win+1)
    df['label']=df['max']/df['close']
#     print(df.head(20))
 
    
    features=df[['vol_volume','vol_price','label']]
    
    return features
    
def build_model():
    print(tf.__version__)
    pass
    


if __name__ == '__main__':
    features = get_feature("sz002118")
    print(features.tail(100))

