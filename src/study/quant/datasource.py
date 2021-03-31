# -*- coding: utf-8 -*-

import pandas_datareader.data as web
import datetime
import matplotlib.pyplot as plt
import mplfinance as mpf
import matplotlib as mpl# 用于设置曲线参数

df = web.get_data_yahoo("002118.SZ", start="2020-01-01", end="2021-03-30")

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

mpf.plot(df, type="candle",mav=(20) , style=get_style(), figscale=5,volume=True)
# mpf.plot(df, type="candle",mav=(20) , style=get_style(), figscale=5,alines={"alines":seq_of_points, "colors":"blue"},volume=True)