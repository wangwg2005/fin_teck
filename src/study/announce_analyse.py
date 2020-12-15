# -*- coding: utf-8 -*-

import os
import json
import time
from _datetime import timedelta
import datetime

anns={}

prices=[]
price_by_day={}

rate=2

def convertPrice(l):
    vs=l.split(",")
    return {"date":vs[0],"index":vs[1],"close":vs[3],"open":vs[6]}

def convertUnit(val):
    if val[-1]=="万":
        return val[:-1]
    elif val[-1]=="亿":
        return str(float(val[:-1])*10000)
    return val

def convertLeverage(l):
    vs=l.split(",")
    obj= {"date":vs[1],"buyinBalance":float(convertUnit(vs[2])),"buyin":float(convertUnit(vs[3])),"repay":float(convertUnit(vs[4]))}
    return obj

leves=[]
leverage={}
with open(u"jl/002118.csv","r",encoding="UTF-8") as f:
    leves=list(map(convertLeverage, f.readlines()))
    for lev in leves:
        leverage[lev["date"]]=lev
    

def get_previous_days(dateStr,tdelta=7):
    timeStruct = time.strptime(dateStr, "%Y-%m-%d")
#转换为时间戳: 
    days=[dateStr]
    timeStamp = int(time.mktime(timeStruct))
    dt=datetime.date.fromtimestamp(timeStamp)
    for i in range(1,tdelta):
        pre_day=dt-datetime.timedelta(i)
    
        
        strTime = pre_day.strftime("%Y-%m-%d") 
        days.append(strTime)
    return days

def test_trade_day(dateStr):
    return dateStr in price_by_day


with open(u"c:\\tmp\\002118.csv","r",encoding="gbk") as f:
    prices=list(map(convertPrice, f.readlines()[2:]))

for  root, dirs, files in os.walk("../cninfo_list", True):
    if root[-7:-3]!='2019':
        continue
    for file in files:
        with open(root+"//"+file,'r',encoding='UTF-8') as f:
            l=f.readline()
            perDay=json.loads(l)
            filtered=list(filter(lambda a:a["secCode"]=='002118',perDay["announcements"]))
            for ann in filtered:
                ann["date"]=file[:-5]
            if len(filtered)>0:
                anns[file[:-5]]=filtered
 

for price in prices:
    price_by_day[price["date"]]=price
    
def analyse_price():
    pass

def analyse_leverage_ann(days, ann_date):
#     print("analysing "+','.join(days))
    start_v=-1
    end_v=-1
    previous_v=-1
    start_date=""
    end_date=""
    leve_msg=""
    price_msg=""
    day_msg=""
    repay_msg=""
    for day in days:
        if not test_trade_day(day):
            continue
        current_v=leverage[day]["buyin"]
        if start_v==-1:
            start_date=day
            start_v=current_v
            leve_msg=str(start_v)
            price_msg=price_by_day[day]["close"]
            repay_msg=str(leverage[day]["repay"])
            day_msg=start_date
        elif current_v*rate<previous_v and previous_v>1000:
            end_v=current_v
            end_date=day
            leve_msg=str(end_v)+" , "+leve_msg
            price_msg=price_by_day[day]["close"] + " , " + price_msg
            repay_msg= str(leverage[day]["repay"]) + " , " + repay_msg
            day_msg=end_date+" , "+day_msg
        else:
            break
             
        previous_v=current_v
    if end_date=="":
        return False
#         end_date=days[1]
#         end_v=leverage[day]["buyin"]
#     print(end_date+"~"+start_date+":"+str(end_v)+"~"+str(start_v))
#     print("days:"+day_msg)
#     print("leverage:"+leve_msg) 
#     print("price:"+price_msg)
#     print("repay:"+repay_msg)
#     print(ann_date+":"+','.join(list(map(lambda a:a["announcementTitle"],anns[ann_date]))))
#     print("")
    return True
        
def analyse_leverage(days):
    pass
    

#leverage analysis

for key, value in anns.items():
    inc=4
    days=get_previous_days(key,inc)
    
    result=False
    first_day=key
    counter=3
    while not result and counter>0:
        days=get_previous_days(first_day, inc)
        result=analyse_leverage_ann(days,key)
        first_day=days[1]
        counter=counter-1
#     analyse_leverage(days)


# price analysis
# for key, value in anns.items():
#     close_price=0
#     open_price=0
#     if key in price_by_day:
#         close_price=float(price_by_day[key]["close"])
#         open_price=float(price_by_day[key]["open"])
#     else:
#         print(key+" is not a trade day1")
#         continue
#         
#     
#     
#     inc=5
#     days=get_previous_day(key,inc)
#     bdate=None
#     for day in days:
#         if day not in price_by_day:
#             continue
#         
#         close_before=float(price_by_day[day]["close"])
#         if close_before<=close_price:
#             bdate=day
#         else:
#             break;
#             
#     if bdate==None:
#         print("no trade date in 5 calenda days")
#         continue
#     if bdate not in price_by_day:
#         continue     
#          
#     open_price=float(price_by_day[bdate]["close"])
#     
#     inc=-1
#     close3=get_previous_day(key,-1)
#     while close3 not in price_by_day:
#         inc=inc-1
#         if inc<-3:
#             print("bad logic")
#             break;
#         close3=get_previous_day(key,inc)
#         
#         
# 
# 
# #     open_price=float(price_by_day[key]["open"])
#         
#     raise_rate=(close_price-open_price)/close_price
#     if raise_rate>0.03:
#         print(bdate+"~"+key+":"+str(raise_rate))
#         print(','.join(list(map(lambda a:a["announcementTitle"],value))))
#         
#         if close3 not in price_by_day:
#             print("the next day is not trade day")
#         else:
#             next_day=price_by_day[close3]
#             open2=float(next_day["open"])
#             close2=float(next_day["close"])
#             rate=(close2-open2)/open2
#             print("raise rate the next day:"+str(rate))
#             
#         print("")
            