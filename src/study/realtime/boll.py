# -*- coding: utf-8 -*-
import yfinance as yf
import numpy as np

price_cache={}

def get_boll(stock_id):
    aapl = yf.Ticker(stock_id)
     
    df = aapl.history(period="20d")
    mean_val=df["Close"].mean();
#     std_var=2*df["Close"].std();
    std2=2*df["Close"].to_numpy().std()
    return mean_val,std2

def realtime_boll(stock_id):
     
    if stock_id in price_cache:
        df=price_cache[stock_id]
    else:
        aapl = yf.Ticker(stock_id)     
        df = aapl.history(period="19d")
     
    close=df["Close"].to_numpy()
    print(close)
    close=np.append(close,20)
    print(close)

print(realtime_boll("000001.SZ"))
            
    
