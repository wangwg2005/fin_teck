# -*- coding: utf-8 -*-

import  pandas as pd
import  math
import  matplotlib.pyplot as plt

df = pd.read_csv('../study/history/000905/000905.csv',index_col=0 , parse_dates=True)
df = df.sort_index()
invest = 100
df['share']=100/df['收盘价']

days = 500

total_share = sum(df[-days:]['share'])
print("shares:"+str(total_share))

total_m = invest*days

price = total_m / total_share
print("last price:" + str(df['收盘价'][-1]))

print("average price:"+str(price))

print("m2")

shares = invest/ df.iloc[-500,2]
cost = invest

avgs=[]

for i in range(1,days):
    p = df.iloc[i-500,2]
    a_p = cost/shares
    avgs.append(a_p)

    adj = math.exp(((a_p / p)-1)*10)
    # adj = a_p / p
    spend = invest * adj
    cost += spend
    shares += spend / p


print(avgs)
print(shares)
print(cost)
print(cost/shares)
plt.plot(avgs)
plt.show()

















