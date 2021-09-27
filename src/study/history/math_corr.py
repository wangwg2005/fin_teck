# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import pandas as pd
from study.history import model_trainer2 as mt
import os

def get_coor(name):
    files=list(map(lambda a:os.path.join(name,a),mt.read_dir(name)))
    prices=mt.read_history(files[0])["2019-12-31":"2020-12-31"];
    
    lever=mt.read_leverage(files[1])["2019-12-31":"2020-12-31"]
    
    df=prices[["收盘价"]]
    df["融资余额"]=lever["融资余额(亿元)"]
    return df.corr()
    
    
if __name__=="__main__":
    names=["csi500","hs300","399006","000016"]
    
    for name in names:
        
        print(get_coor(name))
        print(name)


