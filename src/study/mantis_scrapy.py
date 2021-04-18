# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
from time import sleep
from selenium.common.exceptions import TimeoutException
import datetime

# from selenium.webdriver.chrome.options import Options

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
browser = webdriver.Chrome(options=chrome_options)


def parse_line(s):
    cols = s.split()
    return cols[0], "".join(cols[1:-1]).strip(), cols[-1]


def extract_obj(sec_code, txt):
    ind = txt.rfind(sec_code)


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
    item = {"sec_code": body[0][-7:-1], "sec_name": body[0][0:-10]}
    for pair in body[1:]:
        if len(pair) == 0:
            continue
        kv = pair.split(":")
        item[kv[0]] = kv[1].strip()

    top_buyers = []

    lines = parts[2].split("\n")

    top_sellers = []

    return item


def parse_segment(seg):
    parts = seg.split("\n\n")
    reason = parts[0][:-1]
    items = []
    for i in range(1, len(parts), 5):
        item = parse_item(parts[i:i + 5])
        item["reason"] = reason
        items.append(item)

    return items


def parse_content(txt):
    segments = txt.split('-' * 92)

    part1 = segments[1]
    lines = part1.split("\n")[1:-1]
    for line in lines:
        print(parse_line(line))

    items = []
    for seg in segments[3:]:
        part = seg.strip()
        if len(part) == 0 or part[-1] == '无':
            continue
        items.extend(parse_segment(part))

    for item in items:
        print(item)


def scrap(start_date):

    url = "http://www.szse.cn/disclosure/deal/public/index.html"
    browser.get(url)

    time.sleep(5)

    input_date = browser.find_elements_by_tag_name("input")[13]

    browser.execute_script("arguments[0].value = arguments[1].toString()", input_date, "2021-01-04")

    btn = browser.find_element_by_class_name("txt_btn")
    btn.click()
    time.sleep(5)
    nav1 = browser.find_element_by_id("nav1")
    parse_content(nav1.text)
    browser.close()
