# -*- coding: utf-8 -*-

excep=['交易','余额']

with open("..\\jl\\000300_good.csv","r",encoding="UTF-8") as fin:
    with open("..\\jl\\000300_etled.csv","w",encoding="UTF-8") as fout:
        for l in fin.readlines():
            start2=l[:2]
            if start2 in excep:
                continue
            fout.write(l)
        

