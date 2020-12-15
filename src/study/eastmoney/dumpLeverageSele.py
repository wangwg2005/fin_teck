# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
from time import sleep
from selenium.common.exceptions import TimeoutException
import requests
# from selenium.webdriver.chrome.options import Options

url="http://data.eastmoney.com/rzrq/total/all.html"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
browser=webdriver.Chrome(options=chrome_options)

#browser=webdriver.Chrome()

def get_rows(table):
    rows=table.find_elements_by_tag_name("tr")[2:]
    result=[]
    for row in rows:
        result.append(row.text.split(" "))
        
    return result



def dump_history(code):
    #'http://data.10jqka.com.cn/market/rzrqgg/code/002118/'
    browser.get(url)
    with open("..\\jl\\000300.csv","w",encoding="UTF-8") as f:
        for i in range(1):
            print("page:"+str(i))

            sleep(3)
            table=browser.find_element_by_id("rzrqjyzlTable")
    #         table=tables[-1]
            rows=table.find_elements_by_tag_name("tr")[2:]
            for row in rows:
                l=row.text.replace(" ",",")
                f.write(l+"\n")
    #                 print(row.text.replace(" ",","))
    #         links=browser.find_elements_by_class_name("changePage")
#             nextPage=browser.find_element_by_link_text("下一页")
#             nextPage.click()
            
#         if len(links)==0:
#             return
#         work= links[-1].text=="尾页"
#         if work:
#             links[-2].click()

def get_first_page():
    browser.get(url)
    sleep(3)
    table=browser.find_element_by_id("rzrqjyzlTable")
    rows=get_rows(table)
    
dump_history("123")
print("closed")

# with open("etflist.csv","r",encoding="UTF-8") as f:
# with open(u"C:\\tmp\jl.txt","r",encoding="UTF-8") as f:
#     for l in f.readlines():
#         print(l)
#         values=l.split(",")
#         code=values[0][:6]
#         print("dumping "+values[0]+":"+values[1])
#         dump_history(code)
# 
# print("end")
# browser.close()