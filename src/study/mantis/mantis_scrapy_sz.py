# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
from time import sleep
import datetime
from datetime import timedelta
import logging 
from logging.handlers import RotatingFileHandler
import json

# from selenium.webdriver.chrome.options import Options

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
browser = webdriver.Chrome(options=chrome_options)


logger_name = "example"
logger = logging.getLogger(logger_name)
logger.setLevel(logging.INFO)

log_path = "./mantis_sz.log"
fh = RotatingFileHandler(log_path,maxBytes=50*1024*1024,backupCount=10)
fh.setLevel(logging.INFO)

logger.addHandler(fh)


def output(obj):
    print(obj)
    logger.info(json.dumps(obj))


def parse_line(s):
    cols = s.split()
    return cols[0], "".join(cols[1:-1]).strip(), cols[-1]

def parse_arr(s):
    lines = s.split("\n")
    arrs = map(parse_arr, lines)
    return arrs


def parse_item(parts):
    body_str = parts[0].strip()
    if "\n" in body_str:
        body_str = body_str.replace("\n", "  ")
        body_str = body_str.replace("   ", "  ")
    body = body_str.split("  ")
    item = {"证券代码": body[0][-7:-1], "证券简称": body[0][0:-10]}
    for pair in body[1:]:
        if len(pair) < 2:
            continue
        kv = pair.split(":")
        item[kv[0]] = kv[1].strip()

    

    lines = parts[2].split("\n")
    
    cnames=parse_line(lines[0])
    
    top_buyers = [ dict(zip(cnames,parse_line(l)))   for l in lines[1:] ]
    item[parts[1]]=top_buyers
    
    lines = parts[4].split("\n")    
    top_sellers = [ dict(zip(cnames,parse_line(l)))   for l in lines[1:] ]
    item[parts[3]]=top_sellers

    return item


def parse_segment(seg):
    parts = seg.split("\n\n")
    reason = parts[0][:-1]
    items = []
    for i in range(1, len(parts), 5):
        item = parse_item(parts[i:i + 5])
        item["披露原因"] = reason
        items.append(item)

    return items


def parse_content(txt):
    segments = txt.split('-' * 92)
    
    if len(segments)<2:
        print(txt)
        
    items = []
    for seg in segments[3:]:
        part = seg.strip()
        if len(part) == 0 or part[-1] == '无':
            continue
        items.extend(parse_segment(part))

    return items


def scrap( end_date=None):

    url = "http://www.szse.cn/disclosure/deal/public/index.html"
    browser.get(url)
    time.sleep(5)
    
    
    input_date = browser.find_elements_by_tag_name("input")[13]
    
    
    curr_date= datetime.datetime.strptime(input_date.get_attribute('value'), "%Y-%m-%d")
    
    if end_date is None:
        end_date=str(curr_date)[:10]
        
        
    btn = browser.find_element_by_class_name("txt_btn")
    
    while True:


        time.sleep(5)
        nav1 = browser.find_element_by_id("nav1")
        
        if "没有找到符合条件的文本!" not in nav1.text:
            items=parse_content(nav1.text)
            for item in items:
                item["date"]=str(curr_date)[:10]
                output(item)
        
        
        if end_date== input_date.get_attribute('value'):
            break;
        curr_date = curr_date - timedelta(days=1)
        browser.execute_script("arguments[0].value = arguments[1].toString()", input_date, str(curr_date)[:10])
        
        btn.click()
        
    browser.close()
    
    
scrap(end_date="2021-04-19")

