# -*- coding: utf-8 -*-

import file_cache as fc
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt

def model_train(x,a,b):
    return np.abs(a*np.cos(x/60-0.55)+b+80*np.cos(x/5 *np.pi)-6200)+6200

df=fc.get_from_cache("csi500")
x_data = np.arange(60)
print(x_data)
print(df["中证500"].tolist())
popt, pcov = curve_fit(model_train,x_data,df["中证500"].tolist())
print(popt)
print(pcov)

df["拟合"]=model_train(x_data, *popt)
df.pop("日期")
df.plot()
plt.show()
