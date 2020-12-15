# -*- coding: utf-8 -*-

import os

for  root, dirs, files in os.walk("jl", True):
    for name in files:
        counter=0;
        with open("jl//"+name,'r',encoding="UTF-8") as f:
            ls=f.readlines();
            if len(ls)<2:
                continue
            buyin=list(map(lambda l:float(l.split(",")[3][0:-1]),filter(lambda l:l.find("2020-")>0,ls)))
            for i in range(1,len(buyin)):
                if buyin[i]>=buyin[i-1]*2:
                    counter=counter+1
                    
        print(name[0:6]+":"+str(counter))
