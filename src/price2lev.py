# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

def convertPrice(l):
    vs=l.split(",")
    return {"date":vs[0],"index":vs[1],"close":vs[3]}

def convertLeverage(l):
    vs=l.split(",")
    return {"date":vs[1],"buyinBalance":vs[2],"buyin":vs[3]}

prices=[]
with open(u"c:\\tmp\\002118.csv","r",encoding="gbk") as f:
    prices=list(map(convertPrice, f.readlines()[2:]))

leves=[]
with open(u"jl/002118.csv","r",encoding="UTF-8") as f:
    leves=list(map(convertLeverage, f.readlines()))


def drawLine(a1,b1,a2,b2,num=100):
    plt.figure()
    print("lines in prices:"+str(len(prices)))
    print("lines in prices:"+str(len(leves)))
    if num==-1:
        num=min(len(leves),len(prices))-1
    print(num)
    step=num//11
    xt=range(0,num,step)
    strTick=list(map(lambda ind:leves[ind]["date"], xt))
    strTick.reverse()
    
    x=range(len(leves))[:num]
    y1=list(map(lambda o:float(o["buyinBalance"][:-1]),leves))[:num]
    y1.reverse()
    
#     plt.ylim(a1,b1)
    plt.xticks(xt, strTick)
    plt.plot(x,y1,'b')
    
    y3=list(map(lambda o:float(o["close"]),prices))[:num]
    y3.reverse()
    plt.plot(x,y3,'r')
    
    plt.twinx()
    y2=list(map(lambda o:float(o["buyin"][:-1]),leves))[:num]
    y2.reverse()
    
    
    
    title=prices[num]["date"]+"---"+prices[0]["date"]
    plt.ylim(-10000,30000)
#     plt.plot(x,y2)
    plt.title(title)
    plt.grid()
    plt.show()
    
# drawLine(1800,7800,0,30000,800);

#classic paramters for short term
# drawLine(3000,6000,5000,12000,100);

#classic parameter for long history
drawLine(2000,12000,3000,30000,-1);