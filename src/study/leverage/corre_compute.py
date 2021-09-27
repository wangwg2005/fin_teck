# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
import json
import itertools
from functools import reduce


with open("detail_2019_now.json",'r') as f:
    detail=json.load(f)

duration=30


pd.set_option('display.max_columns', None)


cols=['quant_buttom','quant_top','ratio_top','ratio_buttom']
types=["high","low","close"]

inds=itertools.product(cols,types)

seqs=map(lambda ind:pd.DataFrame(np.array(detail[ind[0]][ind[1]]).T).corr().iloc[:,-1:].add_prefix(ind[0]+"_"+ind[1]),inds)
df=reduce(lambda a,b:pd.concat([a,b],axis=1), seqs)
# for seq in seqs:
#     print(seq)

print(df)



# lv1=map(lambda a:detail[a],detail)
# dfs=[]
# for col in cols:
#     for tp in ["high","low","close"]:
#         data=np.array(detail['quant_buttom']['high']).T
# 
#         df=pd.DataFrame(data)
#         df.corr().to_csv(col+"_"+tp+".csv")
#         dfs.append(object)
    

