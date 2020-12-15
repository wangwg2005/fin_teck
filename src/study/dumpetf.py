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
browser.get('http://data.10jqka.com.cn/market/rzrq/board/etf/')
work=True
with open("etflist.csv","w",encoding="UTF-8") as f:
    while work:
        sleep(3)
        currentPage=browser.find_elements_by_class_name("page_info")[0]
        print("current page:"+currentPage.text)
        tables=browser.find_elements_by_tag_name("table")
        table=tables[1]
        rows=table.find_elements_by_tag_name("tr")[2:]
        for row in rows:
            f.write(row.text.replace(" ",",")+"\n")
            print(row.text.replace(" ",","))

        links=browser.find_elements_by_class_name("changePage")

        work= links[-1].text== "尾页"

        if work:
            links[-2].click()



browser.close()