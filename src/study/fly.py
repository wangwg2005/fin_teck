# -*- coding: utf-8 -*-

import file_cache as fc
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd


def model_train(x,a,b,c,d):
    return a*np.sin(2*np.pi*x/b+c)+d

def fourier(x,y, a):
    sim=np.zeros(len(y))
    pops=[]
    for params in a:
        popt, pcov = curve_fit(model_train,x_data,y-sim,params)
        pops.extend(popt)
        print(popt)
        print(pcov)
        sim+=model_train(x, *popt)
    args=np.array(pops).reshape(len(a),len(pops)//len(a))
    
    return (args,sim)

def predict(x, argums):
    y=np.zeros(len(x))
    for argu in argums:
        y+=model_train(x, *argu)
    return y



def simple_mode(x,a,b):
    return np.sinc(a*x+b)
# 
xx=np.arange(100)
yy=model_train(xx,6000,0.01,5,4)
 
# plt1=plt.plot(xx,yy)
 
 
popt, pcov = curve_fit(model_train, xx,yy,[6000,0.01,5,4])
 
# print(popt)
a = popt[0] 
b = popt[1]
c = popt[2]
d = popt[3]
yvals = model_train(xx,a,b,c,d)
# plot2 = plt.plot(xx, yvals)



csi500=fc.get_from_cache("csi500")
 

date_time = pd.to_datetime(csi500.pop('日期'), format='%Y-%m-%d')
csi500.index=date_time
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
csi500=csi500.sort_index()

start_ind=58

df=csi500[start_ind:91]
# df=df.applymap(lambda a: (a-min_v-wav)/wav)
# print(df)
# 
# # df.plot(grid=True)
x_data = np.arange(len(df))
# # print(x_data)
# # print(df["中证500"].tolist())
args=np.array([[80,10,1,1000] , [100,20,3, -1000] ,[1500,800,-200, -1000]])

y_data=df["中证500"].tolist()

(params, sim)=fourier(x_data, y_data, args)

pred_df=csi500[["中证500"]][start_ind:]

size=len(pred_df)
sim_x=np.arange(size)

sim_y = predict(sim_x, params)
# plt.plot(sim_x,sim_y)
pred_x=np.arange(size,size*2)
pred_y=predict(pred_x, params)

pred_df["pred"]=pred_y
pred_df["sim"]=sim_y
pred_df.plot(grid=True)



plt.show()
