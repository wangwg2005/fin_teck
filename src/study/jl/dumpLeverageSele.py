# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
from time import sleep
from selenium.common.exceptions import TimeoutException
import requests
# from selenium.webdriver.chrome.options import Options

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
browser=webdriver.Chrome(options=chrome_options)

#browser=webdriver.Chrome()


def dump_history(code):
    #'http://data.10jqka.com.cn/market/rzrqgg/code/002118/'
    url="http://data.10jqka.com.cn/market/rzrqgg/code/"+code+"/"
    print(url)
    browser.get(url)
    work=True
    with open('etf\\'+code+".csv","w",encoding="UTF-8") as f:
        while work:
            sleep(3)
            tables=browser.find_elements_by_tag_name("table")
            table=tables[-1]
            rows=table.find_elements_by_tag_name("tr")[2:]
            for row in rows:
                f.write(row.text.replace(" ",",")+"\n")
#                 print(row.text.replace(" ",","))
            links=browser.find_elements_by_class_name("changePage")
            if len(links)==0:
                return
            work= links[-1].text=="尾页"
            if work:
                links[-2].click()
                
#     browser.close()

with open("etflist.csv","r",encoding="UTF-8") as f:
# with open(u"C:\\tmp\jl.txt","r",encoding="UTF-8") as f:
    for l in f.readlines():
        print(l)
        values=l.split(",")
        code=values[0][:6]
        print("dumping "+values[0]+":"+values[1])
        dump_history(code)

print("end")
browser.close()