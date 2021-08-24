# -*- coding: utf-8 -*-
import datetime
from study.leverage import time_util as tutil
from study.leverage import leverage_reader as lreader
import pandas as pd
import matplotlib.pyplot as plt
import os
import mplfinance as mpf

def present(scode):
#     if scode[0]=="6":
#         exc="sse"
#     else:
#         exc="szse"
    exc="cache"
        
    price=pd.read_csv(os.path.join(exc,scode+".csv"),index_col="Date",parse_dates=True)
    lev=pd.read_excel(os.path.join(exc,scode+"_2020.xls"),index_col=0,parse_dates=True)
    
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
#     print(df.head())
# mpf.plot(df, type="candle",mav=(20) , style=get_style(), figscale=5,volume=True)
#     mpf.plot(price, type="candle",mav=(20) , style=get_style(), figscale=5,alines={"alines":seq_of_points, "colors":"blue"},volume=True)
#     price["Volume"]=lev["融资余额(元)"]
    mpf.plot(price, type="candle",mav=(20) , style=get_style(), figscale=5,volume=True)
#     print(lev)
#     lev.plot()
#     plt.show()
present("600438")
    