# -*- coding: UTF-8 -*- 

from statsmodels.tsa.stattools import adfuller
import pandas as pd
import os
from datetime import date

def test(s):
    r = adfuller(s,autolag='AIC')
    return  r[0] < min(r[4].values())
    
counter = 0

result = {}

def test_sid(sid):

    
    file = f'../history/stock/{sid}/price.csv'
    
    if not os.path.exists(file):
        return
    
    df = pd.read_csv(file,index_col=[0], parse_dates=True)[-110:]
    if len(df)< 110:
        print("bad length for "+sid)
        return
    
    r={}
    df1 = df.rolling(5).std().dropna()
    for col in df.columns:
        r[col]=test(df[col])
        r[col+'_std']=test(df1[col])
#     t1=test(df['volume'])

    quant1 =df1.quantile(0.1)
    quant2 =df1.quantile(0.01)
    r['volume_10%']=quant1['volume']
    r['volume_1%']=quant2['volume']
    last = df1['volume'].iat[-1]
    r['volume_std_last'] = last
    
    rate = 3
    
    if last>r['volume_10%']:
        rate = 1
    elif last > r['volume_1%']:
        rate = 2
        
    r['volume_std_rate']=rate
    
    r['close_10%']=quant1['close']
    r['close_1%']=quant2['close']
    
    last =df1['close'].iat[-1]
    r['close_std_last']=last
    
    rate = 3
    
    if last>r['close_10%']:
        rate = 1
    elif last > r['close_1%']:
        rate = 2
        
    r['close_std_rate']=rate
    

    result[sid]=r
        
    
    
if __name__ =='__main__':
    root_dir ='../history/stock'
    for sid in os.listdir(root_dir):
        if sid[0] !='0' and sid[0]!='6':
            continue
        test_sid(sid)

    df=pd.DataFrame(data = result.values(),index= result.keys())
    df['count']=(df[df.columns[:10]].isin([True])).sum(axis=1)
    df = df.sort_values(by='count',ascending=False)
    date_str = str(date.today())[:10]
    df.to_csv(fr'C:\doc\volatility_{date_str}.csv',encoding='UTF8',index_label='sid')
    print(df.head())
    print(f"{counter} stocks passed test")