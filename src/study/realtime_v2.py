# -*- coding: utf-8 -*-


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
from time import sleep
from selenium.common.exceptions import TimeoutException
import requests
import matplotlib.pyplot as plt
from jqka import *
import pandas as pd
import file_cache as fc
from datetime import date
import matplotlib.pyplot as plt

url="http://data.eastmoney.com/rzrq/total/all.html"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
browser=webdriver.Chrome(options=chrome_options)

tmp_dir=r"C:\tmp\program"


def convertUnit(val):
    val=val.replace(",","")
    if val[-1]=="万":
        return float(val[:-1])
    elif val[-1]=="亿":
        return float(val[:-1])*10000
    
    return float(val)

def get_rows(table,skip=2):
    rows=table.find_elements_by_tag_name("tr")[skip:]
    result=[]
    for row in rows:
        cells=row.find_elements_by_tag_name("td")
        values=list(map(lambda a:a.text,cells))
        result.append(values)
        
    return result

def get_csi500_realtime():
    url="http://quotes.money.163.com/trade/lsjysj_zhishu_000905.html"
    browser.get(url)
    sleep(2)
    table=browser.find_element_by_class_name("table_bg001")
    rows=get_rows(table, 1)
    
    rows=list(map(lambda row:[row[0],convertUnit(row[4])], rows))
    df=pd.DataFrame(rows,columns=["日期","中证500"])
    date_time = pd.to_datetime(df.pop('日期'), format='%Y%m%d')
    df.index=date_time
    return df

def get_rzrq_realtime():
    url="http://data.eastmoney.com/rzrq/total/all.html"
    browser.get(url)
    sleep(2)
    table=browser.find_element_by_id("rzrq_history_table")
    #         table=tables[-1]
    rows=get_rows(table)
    rows=list(map(lambda row:[row[0],row[1].strip(),convertUnit(row[3])/10000], rows))
    df=pd.DataFrame(rows,columns=["日期","沪深300","融资余额"])
    date_time = pd.to_datetime(df.pop('日期'), format='%Y-%m-%d')
    df.index=date_time
    return df


import jqka
def deduct_etf():
    total_df=None
    target_etf=["510900","518880","159920","159934"]
#     total_etf=jqka.foreign_ind+jqka.gold_etf
    for code in target_etf:
        time.sleep(5)
        df=None
        try:
            df_raw=fc.get_cache(code, jqka.get_by_code, code)
        except :
            print("error happend when get etf")
            break
        df=df_raw[["融资余额"]].applymap(convertUnit)
        if total_df is None:
            total_df=df
        else:
            total_df=total_df+df
            
    
#             print("total_df",total_df)
#             print("negative df",-total_df)
#             return
    print(total_df)
    return total_df
    
    

def draw_graph():
    
    rzrq=fc.get_cache("rzrq",get_rzrq_realtime)
    
#     print(rzrq)
#     print("rzrq",rzrq)
    csi500=fc.get_cache("csi500",get_csi500_realtime)
#     print("csi500",csi500)

    etf=deduct_etf()/10000
#     print("eft",etf)
    demestic=rzrq-etf

    print("demestic macket",demestic)
    features=rzrq[["沪深300"]]
    features["中证500"]=csi500["中证500"]
#     print(demestic.index.duplicated())
#     features["融资余额"]=demestic["融资余额"]
#     (csi500_value[a]*2.7-1000-rzye[a])*2
    series1=(2.7*csi500["中证500"]-1000-demestic["融资余额"])*2
    print(series1)
    features["买入指数500"]=series1
    series2=(2.7*rzrq["沪深300"]-demestic["融资余额"])*2+5000
    print(features)
    features["买入指数300"]=series2
#     features["沪深300"]=rzrq["沪深300"]
    features.plot(grid=True,title=date.today())
    plt.show()
    
    
#     print(get_csi500_realtime())
#     print(get_rzrq_realtime())
    
    

draw_graph()


