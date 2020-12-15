# -*- coding: utf-8 -*-

import os
import json
import timer
from _datetime import timedelta
import datetime

def convertUnit(val):
    if val[-1]=="万":
        return val[:-1]
    elif val[-1]=="亿":
        return str(float(val[:-1])*10000)
    return val

def convertLeverage(l):
    vs=l.split(",")
    obj= {"date":vs[1],"buyinBalance":convertUnit(vs[2]),"buyin":convertUnit(vs[3]),"repay":convertUnit(vs[4])}
    return obj

leves=[]
leverage={}

def open_leverage(secCode):
    with open(u"jl/"+secCode+".csv","r",encoding="UTF-8") as f:
        leves.extend(list(map(convertLeverage, f.readlines())))
        for lev in leves:
            leverage[lev["date"]]=lev


threshold=3

def print_leverage_jump(secCode):
    open_leverage(secCode)
    for i in range(1, len(leves)):
        if float(leves[i-1]["buyin"])>=threshold*float(leves[i]["buyin"])+1:
            print(f"{leves[i]['date']}~{leves[i-1]['date']} : {leves[i]['buyin']} , {leves[i-1]['buyin']}")
                                                     
    
    
print_leverage_jump("002118")
