# -*- coding: utf-8 -*-

import os
import json
import matplotlib.pyplot as plt

x=[]
y=[]
keyword="被动减持"
for root, dirs, files in os.walk("../cninfo_list", topdown=False):
    for name in files:
        if name[-4:]=="json":
            #print(name)
            with open("../cninfo_list/"+name,'r',encoding="utf-8") as f:
                #l="{\"a\":"+f.readline().replace("'","\"")+"}"
                l=f.readline()
                if len(l)<10 :
                   # t.append(0)
                    continue
                arr=json.loads(l)
                print("ann number:"+str(len(arr)))
                target=list(filter(lambda a:a["announcementTitle"].find(keyword)>-1,arr))
                x.append(name[6:-5].replace("-",""))
                y.append(len(target))
                print(name[:-4]+":"+'.'.join(map(lambda x:x,target)))
                print("target number："+str(len(target)))
      

plt.figure()
plt.plot(x,y)
plt.title(keyword)
plt.show()


          