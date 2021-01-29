# -*- coding: utf-8 -*-

import file_cache as fc
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd

tau = 0.045
def fourier(x, *a):
    ret = a[0] * np.cos(np.pi / tau * x)
    for deg in range(1, len(a)):
        ret += a[deg] * np.cos((deg+1) * np.pi / tau * x)
    return ret


wav=1

def model_train(x,a,b,c,d):
    return a*np.sin(2*np.pi*b*x+c)+d

def simple_mode(x,a,b):
    return np.sinc(a*x+b)
# 
xx=np.arange(100)
yy=model_train(xx,6000,0.01,5,4)
 
# plt1=plt.plot(xx,yy)
 
 
popt, pcov = curve_fit(model_train, xx,yy,[6000,0.01,5,4])
 
print(popt)
a = popt[0] 
b = popt[1]
c = popt[2]
d = popt[3]
yvals = model_train(xx,a,b,c,d)
# plot2 = plt.plot(xx, yvals)



df=fc.get_from_cache("csi500")
 

date_time = pd.to_datetime(df.pop('日期'), format='%Y-%m-%d')
df.index=date_time
# 
# print(df["中证500"].min())
# print()
# 
# min_v=df["中证500"].min()
# max_v=df["中证500"].max()
# wav=(max_v-min_v)/2
# 
# 
# 
df=df.sort_index()[17:58]
# df=df.applymap(lambda a: (a-min_v-wav)/wav)
# print(df)
# 
# # df.plot(grid=True)
x_data = np.arange(len(df))
# # print(x_data)
# # print(df["中证500"].tolist())
popt, pcov = curve_fit(model_train,x_data,df["中证500"].tolist(),[50,200,1,6000])
# print(popt)
# # print(pcov)
# #  
df["拟合"]=model_train(x_data, *popt)
df["diff"]=df["中证500"]-df["拟合"]
# df.pop("日期")
df.plot()
plt.show()
