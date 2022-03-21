# -*- coding: UTF-8 -*- 

import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
from datetime import datetime
import requests

def get_feature(sid):

    sid = 'sz002118'
    today_str = str(datetime.today())[:10]
    print("today str:",today_str)
    data_len = 500
    r = requests.get(f'https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={sid},day,,{today_str},{data_len},qfq').json()
     
    print(r)
    df = pd.DataFrame.from_records(r['data'][sid]['qfqday'],columns=['day','open','close','high','low','volume'])
    
    # df=df[:300]
#    df = pd.read_csv(r'C:\Users\Darren\eclipse-workspace\fin_study\src\study\history\stock\002118\price.csv',encoding='utf8',index_col=[0],parse_dates=True)[-500:];
    
    win =5
    delay =5
    df['vol_price'] = df['close'].rolling(win).std(ddof=0)
    df['vol_volume'] = df['volume'].rolling(win).std(ddof=0)/10000000*2
    df['max5']=df['high'].rolling(5).max().shift(-5+1)
    df['max10']=df['high'].rolling(10).max().shift(-10+1)
    df['label5'] =df['max5']/df['close']
    df['label10'] =df['max10']/df['close']
    df.index=pd.to_datetime(df.pop('day'))

    df['pct']=df['close'].astype(float).pct_change()
    
    
    
    df = df.applymap(lambda a: float(a))
    
    
    print(type(df.iloc[1,0]))
    
    mc = mpf.make_marketcolors(
        up="red",  # 上涨K线的颜色
        down="green",  # 下跌K线的颜色
        edge="black",  # 蜡烛图箱体的颜色
        volume="blue",  # 成交量柱子的颜色
        wick="black"  # 蜡烛图影线的颜色
    )
    df=df.dropna()
    df['color']=df['pct'].map(lambda a: 'red' if a>0 else 'green')
    
    df['s']=df['pct'].map(lambda a: int(a*1000) if a>0 else -int(a*1000))
    df['pct_s']=df['pct'].shift()
    print(df.tail())
    s1 = mpf.make_mpf_style(base_mpl_style="ggplot", marketcolors=mc)
    add_plot=[mpf.make_addplot(df['vol_price'],panel=0,color='red'),mpf.make_addplot(df['vol_volume']/100,panel=0,color='green')]
    mpf.plot(data=df,type="candle",style=s1,volume=True,addplot=add_plot)
    #ax = df[['vol_price','vol_volume','close']].plot(grid=True)
    buy_in = df[df.vol_price<df.vol_volume]
#     df.plot(x='vol_pct',y='pct_s',c=df['color'],kind='scatter')
    plt.show()
    features=df[['vol_volume','vol_price','pct_s']]
    return df
    
if __name__ =='__main__':
    get_feature('sz002118')

