# -*- coding: utf-8 -*-

import requests
from datetime import datetime
import json


# session = HTMLSession()
# url = "http://www.sse.com.cn/disclosure/credibility/supervision/inquiries/"
# h = session.get(url=url)
# h.html.render(sleep=10)
# print(h.html.find("table.table")[0].html)
keys = ['stock_name', 'open', 'close_pre', 'current', 'high', 'low', 'bid_price', 'offer_price', 'vol_share',
        'vol_money',
        'bid_1', 'bid_1_price', 'bid_2', 'bid_2_price', 'bid_3', 'bid_3_price', 'bid_4', 'bid_4_price', 'bid_5',
        'bid_5_price'
    , 'offer_1', 'offer_1_price', 'offer_2', 'offer_2_price', 'offer_3', 'offer_3_price', 'offer_4', 'offer_4_price',
        'offer_5', 'offer_5_price'
    , 'date', 'time']



def get_price_min(stockid,scale=5,datalen=800):
    url = f'http://ifzq.gtimg.cn/appstock/app/kline/mkline?param={stockid},m{scale},,{datalen}&_var=sdata'
    print(url)
    response = requests.get(url)
    res_body = response.text.strip()

    s =res_body[6:]
    
    res = json.loads(s)
    
    if res['code'] !=0 :
        print(res['msg'])
        return None
    
    sdata = res["data"][stockid][f'm{scale}']
    
    return sdata


def get_kline_day(sid,days=20):
    url=f'https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline&param={sid},day,,,{days},qfq&r=0.20250418055060626'
    print(url)
    txt = requests.get(url).text[6:]
    res = json.loads(txt)
    
    if res['code'] !=0 :
        print(res['msg'])
        return None
    
    sdata = res["data"][sid]['qfqday']
    import pandas as pd
    df = pd.DataFrame(sdata,columns=['day','open','close','high','low','volume'])
#     print(df)
    return df
    


def convert_sid(sid):
    return (sid[-2:]+sid[:6]).replace("SS",'sh')
#         return

# rs=search(sse,["2020-02-27","2020-02-24"])
# print(rs)

def split_time_window(stock_id, datalen=800):
    scale = 5  # time window, minutes
    ma = 20
    ma = 'no'
    url = 'http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData'
    param = {'symbol': stock_id, 'scale': scale, 'ma': ma, 'datalen': datalen}
    res = requests.get(url, params=param).json()
    return res

# a =get_kline_day("sh600010")

# get_time_window('sh601006','2021-09-01')
# print(datetime.now().timestamp())
# print(len(split_time_window('sh601006', '2021-09-03')))
