# -*- coding: utf-8 -*-
import yfinance as yf


def get_boll(stock_id):
    aapl = yf.Ticker(stock_id)
     
    df = aapl.history(period="20d")
    mean_val=df["Close"].mean();
    std_var=2*df["Close"].std();
    return mean_val,std_var


print(get_boll("603259.SS"))

