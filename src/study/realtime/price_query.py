# -*- coding: utf-8 -*-

import requests
from datetime import datetime
from json.decoder import JSONDecodeError

# session = HTMLSession()
# url = "http://www.sse.com.cn/disclosure/credibility/supervision/inquiries/"
# h = session.get(url=url)
# h.html.render(sleep=10)
# print(h.html.find("table.table")[0].html)
keys=['stock_name','open','close_pre','current','high','low','bid_price','offer_price','vol_share','vol_money',
      'bid_1','bid_1_price','bid_2','bid_2_price','bid_3','bid_3_price','bid_4','bid_4_price','bid_5','bid_5_price'
      ,'offer_1','offer_1_price','offer_2','offer_2_price','offer_3','offer_3_price','offer_4','offer_4_price','offer_5','offer_5_price'
      ,'date','time']


def get_price(*stockid):
    url='https://hq.sinajs.cn/list={0}'.format(','.join(stockid).lower())

    response=requests.get(url)
    res_body=response.text.strip()
    lines=res_body.split('\n')
    result=[]
    for line in lines:
#         print(line)
        start_ind=line.find('=')
        body=line[start_ind+2:-4]
        infos=body.split(',')

        kv={}
        for i in range(len(keys)):
            kv[keys[i]]=infos[i]
        result.append(kv)
        
    return result

def get_time_window(stock_id,date):
    template='https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_Transactions.getAllPageTime?date={0}&symbol={1}'
    template2='https://vip.stock.finance.sina.com.cn/quotes_service/view/CN_TransListV2.php?num={0}&symbol={1}&rn={2}'
    url=template.format(date, stock_id)
    res=requests.get(url).json()
#     for page in res['detailPages']:
    ts=int(datetime.now().timestamp()*1000)
    url=template2.format(res['detailPages'][10]['page'],stock_id,ts)
    res2=requests.get(url).text
    print(res2)
#         return

proxies=['http://103.242.236.202:8080',
         'http://111.160.169.54:41820',
         'http://114.99.233.47:30001',
         'http://110.83.12.18:57114',
         'http://61.178.149.237:59042'
         ]


def convert_sid(sid):
    return (sid[-2:]+sid[:6]).replace("SS",'sh')
    
def get_history_price(stock_id,day_number=1024,scale=240):
    template="https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol={0}&scale={2}&ma=no&datalen={1}"
    url=template.format(stock_id,day_number,scale)
    print(url)
    try:
        res=requests.get(url)
#         res=requests.get(url)
        res_j=res.json()
        return res_j
    except JSONDecodeError as e:
        print(res.status_code)
        print(res.text)
# rs=search(sse,["2020-02-27","2020-02-24"])
# print(rs)
if __name__=="__main__":
#     print(get_price('sh600618'))
    print(get_history_price('sh000905'))

# get_time_window('sh601006','2021-09-01')
# print(datetime.now().timestamp())