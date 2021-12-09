# -*- coding: utf-8 -*-

import requests
import random
import json
import time

url1="https://xfrtp8762436.sifayun.com/isPoll?{0}"

url2="https://xfrtp8762436.sifayun.com/poll"

template='{"code":"{0}","data":[{"ele_id":"31","poll_ip":"{ip}","poll_case":"","poll_desc":""},{"ele_id":"{2}","poll_ip":"{1}","poll_case":"","poll_desc":""}]}'

date_temp={"ele_id":"31","poll_ip":"220.196.60.35","poll_case":"","poll_desc":""}

random_cases=["1",'2',"3","6","31","39","40"]

ips=["59.36.189.138","112.64.119.194","140.207.23.40"]

ip_db={"sse":"140.206.60.73","szse":"59.36.189.138","csrc":"211.154.210.238",
       "bse":"211.91.160.247","shfe":"58.247.108.124","czce":"118.212.233.175","dce":"218.25.154.94",
       "cffex":"58.32.205.2","cclear":"211.95.52.116","sipf":"211.95.52.85","csf":"119.188.36.27","cfmmc":"211.95.52.116","neeq":"157.0.144.193","sac":"27.221.120.243","cfachina":"27.37.66.111",
       "capco":"59.110.247.151","amac":"163.142.98.136","csits":"60.217.246.239","isc":"140.207.227.251","cscidx":"61.163.80.192","cifcm":"121.36.50.138","ccmi":"183.62.196.101","inverstor":"140.207.227.233","csisc":"59.110.246.125"}



browser_headers1={"content-type": "text/plain; charset=utf-8",    
                 "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
                 "origin": "http://news.sina.com.cn",
                 "referer": "http://news.sina.com.cn/",
                 'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
                 "sec-ch-ua-mobile": "?0",
                 'sec-ch-ua-platform': '"Windows"'
                 }

browser_headers2={"content-type": "application/x-www-form-urlencoded; charset=UTF-8",    
                 "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
                 "origin": "http://news.sina.com.cn",
                 "referer": "http://news.sina.com.cn/",
                 'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
                 "sec-ch-ua-mobile": "?0",
                 'sec-ch-ua-platform': '"Windows"'
                 }

shift={}

def ip_shift(ip):
    
    segs=ip.split(".")
    
    v = int(segs[-1])
    
    genRand = True
    while genRand:
        delta=random.randint(-5,5)
        deltas=[]
        if ip in shift:
            deltas=shift[ip]
            
        if delta not in deltas:
            genRand=False
            deltas.append(delta)
    
    return ".".join([*segs[:3],str(v+delta)])
    
        
if __name__ == "__name__":
    
    for i in range(10):
        for ip in list(ip_db.values())[2:3]:
            time.sleep(random.randint(3,10))
           
            print("old ip",ip)
            
            nip = ip_shift(ip)
            while nip == ip:
                nip = ip_shift(ip)
            
            ip = nip
            url=url1.format(ip)
            a=requests.get(url,headers=browser_headers1).json()
            
            print("nip:",nip)
            
            if a["status"] != 0:
                print("bad result for ip:",ip)
                print(a)
                continue
            
            else:
            
                data={"code":a["code"],"data":[{"ele_id":"31","poll_ip":ip,"poll_case":"","poll_desc":""}]}
                data["data"].append({"ele_id":str(random_cases[random.randint(0,len(random_cases)-1)]),"poll_ip":ip,"poll_case":"","poll_desc":""})
                r=""
    #             print("data:",data)
    #             r = requests.post(url2,data=json.dumps(data).replace(" ",""),headers=browser_headers2)
                print("r",r.text)
                
print(ip_shift("220.196.60.35"))
    