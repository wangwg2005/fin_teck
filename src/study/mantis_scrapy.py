# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
from time import sleep
from selenium.common.exceptions import TimeoutException
import requests
import matplotlib.pyplot as plt
# from selenium.webdriver.chrome.options import Options

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
browser=webdriver.Chrome(options=chrome_options)

def parse_line(str):
    cols = str.split()
    return (cols[0], "".join(cols[1:-1]).strip(), cols[-1])

def extract_obj(sec_code,txt):
    ind=txt.rfind(sec_code)


def parse_content(txt):
    segments=txt.split('-'*20+'\n')

    part1=segments[1]
    lines=part1.split("\n")[1:-1]
    for line in lines:
        print(parse_line(line))



url="http://www.szse.cn/disclosure/deal/public/index.html"
browser.get(url)

time.sleep(5)

input_date=browser.find_elements_by_tag_name("input")[13]

browser.execute_script("arguments[0].value = arguments[1].toString()",input_date,"2021-01-04")

btn=browser.find_element_by_class_name("txt_btn")
btn.click()
time.sleep(5)
nav1=browser.find_element_by_id("nav1")
parse_content(nav1.text)
# browser.close()