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
import math
import model_util

url="http://data.eastmoney.com/rzrq/total/all.html"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
browser=webdriver.Chrome(options=chrome_options)

tmp_dir=r"C:\tmp\program"


def convertUnit(val):
    if type(val)==float:
        return val
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
    df["日期"]=date_time
#     df.index=date_time
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
    df["日期"]=date_time
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
#     print(total_df)
    print("total",total_df)
    return total_df
    
    
def statistics(seri):
    print("diff mean",seri.mean())
    print("diff std",seri.std())


def model1(a):
    return 3000*math.cos(a/60-0.55)+3400+80*math.cos(a/5 *math.pi)

reflect=6200

def mode_std(a):
    return math.fabs(3000*math.cos(a/60-0.55)+3400+80*math.cos(a/5 *math.pi)-reflect)+reflect

def model2(a):
    return math.fabs(2900*math.cos(a/60-0.55)+3500+80*math.cos(a/5 *math.pi)-reflect)+reflect

def model2021(a):
    return math.fabs(3000*math.cos(a/50-0.6)+3400+80*math.cos(a/5 *math.pi)-reflect)+reflect


def model_train(x,a,b,c,d):
    return a*math.cos(b*x+c)+d+80*math.cos(b*x+c)


def predict2():
    leve_csi500 = pd.read_excel("history/融资融券csi500_2021.xls",header=1, encoding="gbk")
    date_time = pd.to_datetime(leve_csi500.pop('交易日期'), format='%Y-%m-%d')
    leve_csi500.index=date_time
    leve_csi500.dropna()
    return model_util.csi500.predict(leve_csi500["融资余额(亿元)"])


def draw_predict(n=70):
    ind=range(n)
    data_m1=list(map(model1,ind))
    data_m2=list(map(model2,ind))
    predict=pd.DataFrame({"model_1":data_m1,"model_2":data_m2})
#     predict=pd.DataFrame({"model_1":data_m1})
#     predict["mode2"]=pd.Series(,name="model2")
    print("predict",predict)
    predict.plot(grid=True)
    plt.show()
    
def draw_graph(risk=True, show_diff=True):
    
    rzrq=fc.get_cache("rzrq",get_rzrq_realtime)
    rzrq.applymap(convertUnit)
#     print(rzrq.info())
    
#     print(rzrq)
#     print("rzrq",rzrq)
    csi500=fc.get_cache("csi500",get_csi500_realtime)
    csi500.applymap(convertUnit)
#     print(csi500.info())
#     print("csi500",csi500)



#     print("demestic macket",demestic)
    features=rzrq[["沪深300"]]
    features["中证500"]=csi500["中证500"]
#     print(demestic.index.duplicated())
#     features["融资余额"]=demestic["融资余额"]
#     (csi500_value[a]*2.7-1000-rzye[a])*2
    
#     print(series1)
    if risk:
        etf=deduct_etf()/10000
#     print("eft",etf)
        demestic=rzrq-etf
        series1=(2.7*csi500["中证500"]-1000-demestic["融资余额"])*2
        features["风险-中证500"]=series1
#     features["sim2"]=predict2()
#     print("rzrq",rzrq)
#     print("demestic",demestic)
#     series2=(2.7*rzrq["沪深300"]-demestic["融资余额"])*2+5000
#     print(features)
#     features["买入指数300"]=series2
#     features["沪深300"]=rzrq["沪深300"]
#     features["融资余额*"]=etf["融资余额"]
    features.pop("沪深300")
    
    features=features.sort_index(axis=0)
    old_index=features.index
    num_ser=range(len(features))
    features.index=num_ser
#     features["sin"]=pd.Series(data=list(map(lambda a:3000*math.cos(a/60-0.55)+3450,num_ser)),name="sin")
#     features["sin2"]=pd.Series(data=list(map(lambda a:3000*math.cos(a/60-0.55)+3350,num_ser)),name="sin")
#     features["sim"]=pd.Series(data=list(map(lambda a:math.fabs(3000*math.cos(a/60-0.55)+3400+80*math.cos(a/5 *math.pi)-6200)+6200,num_ser)),name="sim")

    features["sim"]=pd.Series(data=list(map(model2,num_ser)),name="sim")
    
    if show_diff:
        features["diff"]=features["sim"]-features["中证500"]
        statistics(features["diff"][4:])

    
#     diff_df=features[["diff"]]
# #     diff_df["diff sum"]=diff_df["diff"].cumsum()
#     features.pop("diff")
    features.index=old_index
    features["sim2"]=predict2()
    print(features)
    features.plot(grid=True,title=date.today())
#     
#     
#     diff_df.plot(grid=True)

    
    import os
#     plt.show()
#     plt.rcParams['figure.figsize'] = (16.0, 8.0)
    fig = plt.gcf()
    fig.set_size_inches(16, 8)
    plt.savefig(os.path.join("img",str(date.today())+".png"))
    browser.close()
    browser.quit()
    plt.show()
    
    
#     print(get_csi500_realtime())
#     print(get_rzrq_realtime())
    
    

draw_graph(show_diff=False)

# train_model()
# draw_predict(80)


