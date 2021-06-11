# -*- coding: utf-8 -*-
import pandas_datareader.data as web
import cninfo
import time
import pandas
import matplotlib.pyplot as plt
from datetime import datetime


start_date="2020-01-01"
end_date="2020-12-31"


announces=cninfo.get_by_stock("002118,9900002187", start_date, end_date)["announcements"]

ann_p=[ (ann["announcementTitle"],time.strftime("%Y-%m-%d",time.localtime(ann["announcementTime"]/1000)  ))  for ann in announces ]
# ann_p=[ (ann["announcementTitle"],time.localtime(ann["announcementTime"]/1000))  for ann in announces ]
print(ann_p[0])
df = web.get_data_yahoo("002118.SZ", start=start_date, end=end_date)

df["pre"]=df["Close"].rolling(window=6, min_periods=1).min()
df["aft"]=df["Close"].rolling(window=6, min_periods=1).min().shift(-6)
df["x"]=df["Close"]/df["pre"]-1
df["y"]=df["Close"]/df["aft"]-1
print(df.head(10))


# df=df[6:-6]

x=[]
y=[]
txt=[]

for ann in ann_p:
    txt.append(ann[0])
    ind=ann[1]
    if ind not in df.index:
        ind=list(df[ind:].index)[0]
    x.append(df.loc[ind]["x"])
    y.append(df.loc[ind]["y"])
    
        

plt.scatter(x,y)

for i in range(len(x)):
    plt.annotate(txt[i], xy = (x[i], y[i]), xytext = (x[i]+0.001, y[i]+0.001))
    
    
plt.show()

