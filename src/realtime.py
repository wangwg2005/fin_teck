# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
from time import sleep
from selenium.common.exceptions import TimeoutException
import requests
import matplotlib.pyplot as plt
# from selenium.webdriver.chrome.options import Options

url="http://data.eastmoney.com/rzrq/total/all.html"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
browser=webdriver.Chrome(options=chrome_options)

tmp_dir=r"C:\tmp\program"

def get_rows(table,skip=2):
    rows=table.find_elements_by_tag_name("tr")[skip:]
    result=[]
    for row in rows:
        result.append(row.text.split(" "))
        
    return result


category_keyword={}



def get_csi500_realtime():
    url="http://quotes.money.163.com/trade/lsjysj_zhishu_000905.html"
    browser.get(url)
    sleep(2)
    table=browser.find_element_by_class_name("table_bg001")
    rows=get_rows(table, 1)
    
    return rows

def get_rzrq_realtime():
    url="http://data.eastmoney.com/rzrq/total/all.html"
    browser.get(url)
    sleep(2)
    table=browser.find_element_by_id("rzrq_history_table")
    #         table=tables[-1]
    rows=get_rows(table)
    return rows

def get_etf_leverage(code):
    
    pass

def draw_lines(a1,b1,a2,b2):
    appendToday=False
    csiCurr=5073.65
    hsCurr=1000
    leve=1000
    
    print("retrieving csi500 data")
    csi500=get_csi500_realtime()
    print("retrieving rzrq data")
    rzrq=get_rzrq_realtime()
    browser.close()
    
    print("drawing image")
    size=min(len(csi500),len(rzrq))
#     size=len(rzrq)
    print("csi500:",str(len(csi500)))
    print("hs3000:",str(len(rzrq)))
    
        
    t1=csi500[:size]
    t1.reverse()
#     t1=[]
    t2=rzrq[:size]
    t2.reverse()
    
    x=[]
    if appendToday:
        x=range(size+1)
        t2.append(t2[-1])
    else:
        x=range(size)
    
    
    csi500_value=list(map(lambda a:float(a[4].replace(',','')),t1))
    if appendToday:
        csi500_value.append(csiCurr)
    hs300=list(map(lambda a:float(a[1]),t2))
    
#     print(rzye)
    plt.figure(num=t2[-1][0])
    plt.ylim(a1,b1)
    plt.plot(x,csi500_value,'r')
    plt.plot(x,hs300,'r')
    
    
    plt.twinx()
    plt.ylim(a2,b2)
     
 
    rzye=list(map(lambda a:float(a[3]),t2))
    plt.plot(x,rzye,'b')
     
     
    model500_v=list(map(lambda a:(csi500_value[a]*2.7-1000-rzye[a])*2,x))
    plt.plot(model500_v)
     
#     y8=list(map(lambda a:(hs300[a]*2.7+11000-rzye[a])*2,x))
#     plt.plot(x,y8)
    
    xticks=list(range(size-1,0,-5))
    xticks.reverse()
    labels=list(map(lambda a:t2[a][0], xticks))
    plt.xticks(xticks, labels)
    
    plt.grid()
    plt.show()
    
draw_lines(0,12000,0,15000);
# def compute_value(csi500,levera):
#     print((csi500*2.7-1000-levera)*2)
     
# print(compute_value(5270,10426.41))

