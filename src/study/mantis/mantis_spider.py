# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
from time import sleep
from selenium.common.exceptions import TimeoutException
import requests
import matplotlib.pyplot as plt
import file_cache as fc
import logging
from logging.handlers import RotatingFileHandler 
import json
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options


# create logger
logger_name = "example"
logger = logging.getLogger(logger_name)
logger.setLevel(logging.DEBUG)

log_path = "./output.log"
fh = RotatingFileHandler(log_path,maxBytes=50*1024*1024,backupCount=10)
fh.setLevel(logging.INFO)

logger.addHandler(fh)



chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
browser=webdriver.Chrome(options=chrome_options)


def output(obj):
    logger.info(json.dumps(obj))


def scrap_sh(start_date=None,date_str=""):
    url="http://www.sse.com.cn/disclosure/diclosure/public/dailydata/"
    browser.get(url)
    
    work=True
    
    
    if start_date is not None:
        time.sleep(5)
        start=browser.find_element_by_id("start_date2")
        btn=browser.find_element_by_id("btnQuery")
        browser.execute_script("arguments[0].value=arguments[1].toString()",start,start_date)
        btn.click()
    
    while work:
        time.sleep(5)
        today=browser.find_element_by_class_name("pageDate").text
        work= not today== date_str
        
        top=browser.find_element_by_class_name("dailyData")
        try:
            if top.find_element_by_tag_name("td") is None :
                continue
        except:
            print("bad date:"+today)
            
            if work:
                browser.find_element_by_id("preBtn").click()
            continue
        
    
        but=browser.find_element_by_css_selector(".public_texthre > a")
        but.click()
        
        time.sleep(1)
        
        titles = browser.find_elements_by_class_name("sse_subtitle_1")
        datas = browser.find_elements_by_class_name("sse_second_cn_con")
        
        for types in range(len(datas)):
            table=datas[types]
            col_names=[]
            for col_name in table.find_elements_by_tag_name("th"):
                col_names.append(col_name.text)
            
            items=[]
            for row in table.find_elements_by_tag_name("tr")[1::9]:
                item={"日期":today}
#                 print(row.text)
                cols=row.find_elements_by_tag_name("td")
                
                len_col=len(cols)
                if len_col==1:
                    continue
                if len_col!=len(col_names):
                    print("bad length")
                    for c in cols:
                        print(c.text)
                for i in range(len_col):
                    item[col_names[i]]=cols[i].text
                    
                item["原因"]=titles[types].text
                items.append(item)
                    
            
            mantis_list=[]
            ind=0
            for nested_table in table.find_elements_by_class_name("search_"):
                rows = nested_table.find_elements_by_tag_name("tr")
                
                sub_col_names=[]

                for col_name in rows[0].find_elements_by_tag_name("td"):
                    sub_col_names.append(col_name.text)
                
                for i in range(1,len(rows)):
                    row=rows[i]
                    cols=row.find_elements_by_tag_name("td")
                    if len(cols)==1:
                        continue
                    
                    
                    mantis={}
                    for j in range(len(cols)):
                        if len(sub_col_names)==0:
                            continue
                        mantis[sub_col_names[j]]=cols[j].text
                
                    mantis_list.append(mantis)
                    
                items[ind]["详情"]=mantis_list
                ind+=1
                
            if len(items)>0:
                output(items)
        
        if work:
            pre_btn=browser.find_element_by_id("preBtn")
            try:
                cover= browser.find_element_by_class_name("row mobile_flex")
                wait = WebDriverWait(browser,60);
                wait.until(EC.invisibility_of_element(cover));
                
                
                wait.until(EC.element_to_be_clickable(pre_btn ));
            except:
                pass
            pre_btn.click() 

        else:
            browser.close()
        
scrap_sh(start_date="2021-03-23",date_str="2019-01-01")


# def compute_value(csi500,levera):
#     print((csi500*2.7-1000-levera)*2)
     
# print(compute_value(5270,10426.41))

