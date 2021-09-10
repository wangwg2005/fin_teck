# -*- coding: utf-8 -*-
import yfinance as yf
import numpy as np

price_cache={}

def get_boll(df):
    mean_val=df["Close"].mean();
#     std_var=2*df["Close"].std();
    std2=2*df["Close"].to_numpy().std()
    return mean_val,std2

def realtime_boll(stock_id, current_price):
     
    if stock_id in price_cache:
        close=price_cache[stock_id]
    else:
        aapl = yf.Ticker(stock_id)     
        close = aapl.history(period="19d").to_numpy()
        price_cache[stock_id]=close
        
    
    close=np.append(close,current_price)
    
    return close.mean(),2*close.std()


def test():
    ticker = yf.Ticker('600958.SS')
#     print(ticker.info)
    df=ticker.history(period='21d')[:20]
    print(df)
    boll=get_boll(df)
    print(boll[0]+boll[1])
    
# test()
# print(realtime_boll("000001.SZ"))
            
    
