# -*- coding: utf-8 -*-

from requests_html import HTMLSession,HTML
import numpy as np
import pandas as pd

session = HTMLSession()


gold_etf=["518880","518800","159937","159934"]
foreign_ind=["510900","513100","513090","513660","513030","159941","513500"]


def get_by_code(code):
    
    print("retriveing ",code)
    
    url = "http://data.10jqka.com.cn/market/rzrqgg/code/"+code
    h = session.get(url=url)
    
    ##这个脚本有问题
    
    cname=["序号","日期","融资余额", "融资买入额","融资偿还额","融资净买入","融券余量","融券卖出量","融券偿还量","融券净卖出","融资融券余额"]
    h.html.render(sleep=5)
    tables=h.html.find(".m-table")
    if len(tables)<2:
        print("no table exists")
    table=tables[1]
    rows=table.find("tr")[2:]
    df=pd.DataFrame(list(map(lambda row:row.text.split("\n"),rows)),columns=cname)
    df.pop("序号")
    date_time = pd.to_datetime(df.pop('日期'), format='%Y-%m-%d')
    df["日期"]=date_time
    return df
#     for row in rows:
#         print(row.text.replace("\n",":"))
        
# arr=np.array(get_by_code("510900"))
# print(arr[:,2])