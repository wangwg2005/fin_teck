# -*- coding: utf-8 -*-
import business_day
import pandas as pd
from datetime import date
import os 

def dump(sid):
    
    days=pd.date_range(end=date.today(),periods=6,freq=business_day.get_business_day_cn("all"))[:-1]
    days = list(map(lambda day: day.strftime('%Y%m%d'),days))
    
    print(days)

    root_dir='../../data'
    sid_dir=os.path.join(root_dir,sid);
    if not os.path.exists(sid_dir):
        os.makedirs(sid_dir)
    elif len(os.listdir(sid_dir))>0:
        last_date = max(os.listdir(sid_dir))[:8]
        if last_date > days[0]:
            days=days[days.index(last_date):][1:]
            
    if sid[0]=='6':
        sid ='0'+sid
    else:
        sid ='1'+sid
    
    print(days)
    for day in days:
        print(day)
        url = f'http://quotes.money.163.com/cjmx/{day[:4]}/{day}/{sid}.xls'
        print("requesting trade detail from "+url)
        df = pd.read_excel(url)
        df.to_csv(os.path.join(sid_dir,day+".csv"),encoding='utf8',index=False);
        
# def analyze(df):
    
        
dump('002118')
dump('600227')