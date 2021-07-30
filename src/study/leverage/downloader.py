# -*- coding: utf-8 -*-

import requests
import tempfile
import os

userAgent="User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"


sse_url='http://www.sse.com.cn/market/dealingdata/overview/margin/a/rzrqjygk{0}.xls'

szse_url='http://www.szse.cn/api/report/ShowReport?SHOWTYPE=xlsx&CATALOGID=1837_xxpl&txtDate={0}&tab2PAGENO=1&random=0.8927812381738702&TABKEY=tab2'
szse_index='http://www.szse.cn/disclosure/margin/margin/index.html'


#"20210624"
def download_leverage_sse(date_str):
    url=sse_url.format(date_str)
    print(url)
    
    fpath=os.path.join('sse','rzrqjygk'+date_str+'.xls')
    
    download(url, fpath)
    
    
def download(url,target_path=None):
    
    r = requests.get(url, headers={
            "User-Agent": userAgent
        }, stream=True)
    if r.status_code!=200:
        print(r.status_code)
        print(r.text)
        return
    if target_path==None:
        fp, fpath = tempfile.mkstemp(suffix=".PDF")
        with os.fdopen(fp, 'wb') as fd:
            for chunk in r.iter_content(1024*1024):
                fd.write(chunk)
        r.close()
        return fpath
    else:
        with open(target_path,'wb')as f:
            for chunk in r.iter_content(1024*1024):
                
                f.write(chunk)
        r.close()
        
def download_leverage_szse(date_str):
    url=szse_url.format(date_str)
    print(url)
    
    fpath=os.path.join('szse','rzrqjygk'+date_str+'.xls')
    if os.path.exists(fpath):
        print("file exists, skip")
    else:
        download(url, fpath)
    
    