# -*- coding: utf-8 -*-
import calendar
from datetime import datetime, date, timedelta
holiday=[]

def stringfy(date):
    return str(date).replace("-","")

def skip_holiday(day):
    while str(day) in holiday:
        day=day+timedelta(-1)
        
    return day

def get_prevous_trade_date(currentdate):
    
    
    year= currentdate.year
    month = currentdate.month
    day = currentdate.day
    weekday=calendar.weekday(year,month,day)
    
    result=None
    if weekday==0:
        result=currentdate+timedelta(-3)
    else:
        result=currentdate+timedelta(-1)
        
    result=skip_holiday(result)
            
    return result