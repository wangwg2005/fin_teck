# -*- coding: utf-8 -*-

import requests
from datetime import datetime

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


def get_price(*stockid):
    url = 'https://hq.sinajs.cn/list={0}'.format(','.join(stockid))

    response = requests.get(url)
    res_body = response.text.strip()

    lines = res_body.split('\n')
    result = []
    for line in lines:
        start_ind = line.find('=')
        body = line[start_ind + 2:-4]
        infos = body.split(',')

        kv = {}
        for i in range(len(keys)):
            kv[keys[i]] = infos[i]
        result.append(kv)

    return result


def get_time_window(stock_id, date):
    url1 = 'https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_Transactions.getAllPageTime'
    url2 = 'https://vip.stock.finance.sina.com.cn/quotes_service/view/CN_TransListV2.php'
    param1 = {'date': date, 'symbol': stock_id}

    res = requests.get(url1, params=param1).json()
    #     for page in res['detailPages']:
    ts = int(datetime.now().timestamp() * 1000)
    param2 = {'num': res['detailPages'][10]['page'], 'symbol': stock_id, 'rn': ts}
    res2 = requests.get(url2, params=param2).text
    print(res2)


#         return

# rs=search(sse,["2020-02-27","2020-02-24"])
# print(rs)

def split_time_window(stock_id, datalen=1023):
    scale = 5  # time window, minutes
    ma = 20
    url = 'http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData'
    param = {'symbol': stock_id, 'scale': scale, 'ma': ma, 'datalen': datalen}
    res = requests.get(url, params=param).json()
    return res


# get_time_window('sh601006','2021-09-01')
# print(datetime.now().timestamp())
# print(len(split_time_window('sh601006', '2021-09-03')))
