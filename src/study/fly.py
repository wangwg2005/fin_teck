# -*- coding: utf-8 -*-

import file_cache as fc
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd

tau = 0.045
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


def model_train(x,a,b,c,d):
    return a*np.sin(2*np.pi*b*x+c)+d



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
df=csi500[17:58]
# df=df.applymap(lambda a: (a-min_v-wav)/wav)
# print(df)
# 
# # df.plot(grid=True)
x_data = np.arange(len(df))
# # print(x_data)
# # print(df["中证500"].tolist())
args=np.array([[8,5,1,1000] , [1000,800,10, -3000]])

y_data=df["中证500"].tolist()

(params, sim)=fourier(x_data, y_data, args)

plt.plot(sim)


# popt, pcov = curve_fit(model_train,x_data,df["中证500"].tolist(),[8,5,1,1000])
# print(popt)
# # # print(pcov)
# # #  
# df["拟合"]=model_train(x_data, *popt)
# df["diff"]=df["中证500"]-df["拟合"]
# 
# popt1, pcov = curve_fit(model_train,x_data,df["diff"].tolist(),[1000,800,10,-3000])
# print(popt1)
# 
# sim_x= np.arange(len(df)+20)
# df["sim2"] = model_train(x_data, *popt1)
# df["sim"]=model_train(x_data, *popt1)+model_train(x_data, *popt)
# df.pop("diff")
# df.pop("sim2")
# df.pop("拟合")
# # df.pop("日期")
# # df.plot()
# 
# pred_df=pd.DataFrame({"sim":model_train(sim_x, *popt1)+model_train(sim_x, *popt)})
# pred_df["close"]=csi500["中证500"][17:17+len(pred_df)].tolist()
# pred_df.plot(grid=True)

plt.show()
