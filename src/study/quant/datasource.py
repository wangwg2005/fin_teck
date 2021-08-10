# -*- coding: utf-8 -*-

import yfinance as yf
import mplfinance as mpf
import matplotlib as mpl# 用于设置曲线参数

aapl = yf.Ticker("603259.SS")

df = aapl.history(period="1y")

def get_style():
    mc = mpf.make_marketcolors(
        up='red', 
        down='green', 
        edge='i', 
        wick='i', 
        volume='in', 
        inherit=True)
    
    style = mpf.make_mpf_style(base_mpl_style="ggplot", marketcolors=mc)
    return style
print(df.head())
# mpf.plot(df, type="candle",mav=(20) , style=get_style(), figscale=5,volume=True)
# mpf.plot(df, type="candle",mav=(20) , style=get_style(), figscale=5,alines={"alines":seq_of_points, "colors":"blue"},volume=True)