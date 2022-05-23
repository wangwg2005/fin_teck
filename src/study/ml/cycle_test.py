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

def test_df(price_df):
    train_len = 35
    df = price_df[-train_len:]
    df['lev_ratio']=2*df['rzmr']/((df['high']+df['low'])*df['volume'])
    if len(df)< train_len:
        print("bad length")
        return
    
    r={}
    df1 = df.rolling(5).std().dropna()
    for col in df.columns:
        r[col]=test(df[col])
        r[col+'_std']=test(df1[col])
#     t1=test(df['volume'])

    r['volume_10%']=df1['volume'].quantile(0.1)
    r['volume_1%']=df1['volume'].quantile(0.01)
    
    last = df1['volume'].iat[-1]
    r['volume_std_last'] = last
    
    rate = 3
    
    if last>r['volume_10%']:
        rate = 1
    elif last > r['volume_1%']:
        rate = 2
        
    r['volume_std_rate']=rate
    
    r['close_10%']=df1['close'].quantile(0.1)
    r['close_1%']=df1['close'].quantile(0.01)
    
    last =df1['close'].iat[-1]
    r['close_std_last']=last
    
    rate = 3
    
    if last>r['close_10%']:
        rate = 1
    elif last > r['close_1%']:
        rate = 2
        
    r['close_std_rate']=rate
    
    r['lev_10%'] = df['lev_ratio'].quantile(0.9)
    r['lev_1%'] = df['lev_ratio'].quantile(0.99)
    
    last = df['lev_ratio'].iat[-1]
    
    rate = 1
    if last> r['lev_1%']:
        rate = 3
    elif last>r['lev_10%']:
        rate =2
    
    r['lev_ratio_last']=last
    r['lev_ratio_rate'] = rate

    return r

def test_sid(sid):

    
    file = f'../history/stock/{sid}/price.csv'
    fpath = os.path.join(os.path.dirname(__file__),file)
    
    if not os.path.exists(fpath):
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
    

    return r
        
def test_all(): 
    root_dir ='../history/stock'
    path = os.path.join(os.path.dirname(__file__),root_dir)
    print(path)
    for sid in os.listdir(path):
        if sid[0] !='0' and sid[0]!='6':
            continue
        result[sid] = test_sid(sid)

    df=pd.DataFrame(data = result.values(),index= result.keys())
    df['count']=(df[df.columns[:10]].isin([True])).sum(axis=1)
    return df
#     df = df.sort_values(by='count',ascending=False)
#     date_str = str(date.today())[:10]
#     buffer = df.to_json(orient="records")
#     base_dir = r'C:\Users\Darren\eclipse-workspace\fin_study\src\javascript\js\data'
#     with open( os.path.join(base_dir,f'volatility_{date_str}.js'),'w') as fo:
#         fo.write('records = ')
#         fo.write(buffer)
#     
#     
#     report_path = fr'C:\doc\volatility_{date_str}.csv'
#     df.to_csv(report_path,encoding='UTF8',index_label='sid')
#     
#     print(df.head())
#     print(f"report generated at {report_path}")   
    
if __name__ =='__main__':
    test_all()