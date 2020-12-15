# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

def convert(l):
    vs=l.split(",")
    return {"date":vs[0],"index":vs[1],"rzrq":vs[-4],"volatility":vs[2],'ratio':vs[5]}

def convertCsi500(l):
    vs=l.split(",")
    return {"date":vs[0],"close":float(vs[3])}

ls=[]
with open(u"000300_etled.csv","r",encoding="UTF-8") as f:
    ls=list(map(convert, f.readlines()))

csi500=[]
with open(u"000905_1.csv","r",encoding="gbk") as f:
    csi500=list(map(convertCsi500, f.readlines()))


def drawLine(a1,b1,a2,b2,num=100):
    plt.figure()
    if num==-1:
        num=len(ls)-1
    
    step=num//11
    xt=range(0,num,step)
    strTick=list(map(lambda ind:ls[ind]["date"], xt))
    strTick.reverse()
    
    x=range(num)
    x1=ls[:num]
    x1.reverse()
    
    y1=list(map(lambda o:float(o["index"]),x1))
    
    plt.ylim(a1,b1)
    plt.xticks(xt, strTick)
    plt.plot(x,y1,'r')
    
    y3=list(map(lambda o:float(o["close"]),csi500[:num]))
    y3.reverse()
    plt.plot(x,y3,'r')
    
    print(ls[num])
    plt.twinx()
    
    #draw leverage
    y2=list(map(lambda o:float(o["rzrq"]),ls))[:num]
    y2.reverse()
    
    
    y7=list(map(lambda a:(y3[a]*2.7-1000-y2[a])*2,x))
    y8=list(map(lambda a:(y1[a]*2.7+11000-y2[a])*2,x))
 
    plt.ylim(a2,b2)
    plt.plot(x,y2)
    plt.plot(x,y7)
    plt.plot(x,y8)
    
    
    for i in x:
        if y7[i]<5500:
            m=max(y3[i:i+60])
            
            print(x1[i]["date"]+":"+str(y3[i])+":"+str(((m-y3[i])/y3[i])))
#             print(x1[i]["date"]+":"+','.join(map(lambda f:str(f),y3[i:i+30])))



#draw volatility
#     y4=list(map(lambda o:float(o["volatility"]),x1))
#     y5=[]
#     for i in range(num,0,-1):
#         print(i)
#         t1=float(csi500[i]["close"])
#         t0=float(csi500[i-1]["close"])
#         y5.append((t0/t1-1)*100)
#         
#     y6=[]
#     for i in range(num,0,-1):
#         print(i)
#         t1=float(ls[i]["rzrq"])
#         t0=float(ls[i-1]["rzrq"])
#         y6.append((t0/t1-1)*100)
#         
#     plt.ylim(-10,10)
#     print(len(y4))
#     print(len(y5))
#     plt.plot(x,y4,'g')
#     plt.plot(x,y5,'b')
#     plt.plot(x,y6,'r')





    title=ls[num]["date"]+"---"+ls[0]["date"]
    plt.grid()
    plt.title(title)
    
    plt.show()


def draw_ratio(a1,b1,a2,b2,num=100):
    plt.figure()
    if num==-1:
        num=len(ls)-1
    
    step=num//11
    xt=range(0,num,step)
    strTick=list(map(lambda ind:ls[ind]["date"], xt))
    strTick.reverse()
    
    x=range(num)
    x1=ls[:num]
    x1.reverse()
    
    y1=list(map(lambda o:float(o["index"]),x1))
    
    plt.ylim(a1,b1)
    plt.xticks(xt, strTick)
    plt.plot(x,y1,'r')
    
    y3=list(map(lambda o:float(o["close"]),csi500[:num]))
    y3.reverse()
    plt.plot(x,y3,'r')
    
    print(ls[num])
    plt.twinx()
    
    #draw leverage
    y2=list(map(lambda o:float(o["ratio"].replace('%','').replace('-','0')),ls))[:num]
    y2.reverse()
    plt.ylim(0,6)
    plt.plot(x,y2)
    plt.show()
    
# drawLine(1800,7800,0,30000,800);

# classic paramters for short term
# drawLine(3000,6000,5000,12000,100);

#classic parameter for long history
drawLine(2000,12000,3000,30000,1200);

# draw_ratio(2000,12000,3000,30000,1500);


