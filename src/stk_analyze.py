# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

import pandas as pd


def convertUnit(val):
    if type(val)==float:
        return val
    if val[-1]=="万":
        return val[:-1]
    elif val[-1]=="亿":
        return str(float(val[:-1])*10000)
    return val

def rongzie(series):
    return series["融券卖出量"]*series["融券卖出量"]

stk=pd.read_csv(r"C:\Users\Darren\eclipse-workspace\fin_study\src\data\002118_ori.csv",encoding="utf8")
pri=pd.read_csv(r"C:\Users\Darren\eclipse-workspace\fin_study\src\data\002118.csv",encoding="gbk")


len=200


# print(pri[["日期","收盘价"]][:len])
# print(stk)
date_time = pd.to_datetime(stk.pop("日期"), format='%Y-%m-%d')
# stk.applymap(convertUnit)
# features=stk[["融资买入额"]][:400]"融资买入额",
features=stk[["融资买入额","融资偿还额"]][:len].applymap(convertUnit)
features=features.astype(float,float)

features["买入额"]=features["融资买入额"].shift(1)
features["偿还额"]=features["融资偿还额"].shift(1)



ft=pri[["涨跌幅"]][:len].applymap(lambda x:float(x)*2000+1000)
ft=ft.astype(float)
ft["融资买入"]=(features["融资买入额"]/features["买入额"]-1)*20000
# ft["融资偿还"]=(features["融资偿还额"]/features["偿还额"]-1)*20000

# features["涨跌幅"]=pri["涨跌幅"][:400].map(lambda x:float(x)*2000+1000)

# # features["融券卖出额"]=
# # features=features[:300]
# features.index=date_time[:400]
# print(features)
# print(pri["涨跌幅"])

print(ft)
print(ft.dtypes)
ft.plot()
plt.show()
