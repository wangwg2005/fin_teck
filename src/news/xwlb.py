# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests

def demo(url):
    
    
    resp=requests.get(url)
    resp.encoding="utf-8"
    
    soap=BeautifulSoup(resp.text)
    
    txt=soap.find(id="about_txt")
    
    for s in txt.strings:
        print(s)
    
demo("https://tv.cctv.com/2021/10/20/VIDEC9rcAwir8LX8qIHh1cUf211020.shtml?spm=C31267.PFsKSaKh6QQC.S71105.19")