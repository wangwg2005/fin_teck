# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

ind_list=pd.read_csv("etflist.csv",usecols=[1,2],names=["code","name"],dtype=object)
# ind_list.columns=["code","name"]

def filter_out_main():
    ind_list.index=ind_list["name"].map(str.strip)
    inds=ind_list.filter(regex="(500|300)", axis=0)
#     inds=inds.filter(regex="^(?!标普500)")
    return inds

def filter_by_code():
    ind_list.index=ind_list["code"].map(str.strip)
    inds=ind_list.filter(like="510050")
    return inds
    
def filter_out_gold():
    ind_list.index=ind_list["code"].map(str.strip)
    inds=ind_list[ind_list["name"].str.contains("黄金")]
    return inds
#     inds=inds.filter(regex="^(?!标普)")2
# inds=filter_out_main()
inds=filter_out_main()
# inds=filter_by_code()
print("targets:")
print(inds)
print("------targets:")

def convert(val_str):
    if type(val_str)==float:
        return val_str
    if val_str[-1]=='亿':
        return float(val_str[:-1])*100000000
    if val_str[-1]=='万':
        return float(val_str[:-1])*10000

df_all=None
print("codes")
print(inds["code"].values)
# dfs=list(map(lambda code:pd.read_csv("etf/"+str(code)+".csv",usecols=[1,2,5]),inds["code"].values))
for code in inds["code"].values:
    code_str=str(code)
#     if code!='510050':
#         continue
    if code_str=="513500":
        continue
    df=pd.read_csv("etf/"+code_str+".csv",usecols=[1,2,10])
    df.columns=["date","call","all"]
    date_time = pd.to_datetime(df.pop('date'), format='%Y-%m-%d')
    df.index=date_time
    df["call"]=df["call"].map(convert)
    df["all"]=df["all"].map(convert)
    df["put"]=df["all"]-df["call"]
    df.pop("all")
#     df[code_str+"_call"]=df["call"].map(convert)
#     df[code_str+"_put"]=df["put"].map(convert)
#     df.pop("call")
#     df.pop("put")
#     print(code)
#     print(df[:10])
    if df_all is None:
        df_all=df
    else:
        df_all=df_all.join(df,how='left', lsuffix='', rsuffix='_'+code_str)
        
print("all---")
pd.set_option('display.max_columns', None)
print(df_all[-40:])

df_all=df_all[:1000]
call_column=df_all.loc[:, df_all.columns.str.startswith('call')]
put_column=df_all.loc[:, df_all.columns.str.startswith('put')]
# call_column.plot()
print("call columns:")
print(call_column[:10])
print("put columns:")
print(put_column[:10])
# put_column.plot()

call_sum=call_column.sum(axis=1)
put_sum=put_column.sum(axis=1)
print("call------")
print(call_sum)
print("put------")
print(put_sum)

plt.plot(call_sum)
plt.plot(put_sum)
# sum_row.plot()
plt.show()
