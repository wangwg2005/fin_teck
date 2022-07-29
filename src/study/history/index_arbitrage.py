# -*- coding: utf-8 -*-
import pandas as pd
import os

def get_feature(name):
    start = "2020-02-01"

    df = pd.read_csv(os.path.join(name,name+".csv"),encoding="utf8",parse_dates=[0],index_col=0,nrows=4000).sort_index()[start:]
    return df['涨跌幅'].map(float)


if __name__ == "__main__":
    indexes = ["000016","000300","000688","399006","000905"]
#     indexes = ["000016","000688"]
    
    features = list(map(get_feature, indexes))
#     print(features[0])
    size = len(features[0])
    
    m = [[[ f0[i]-f1[i] for f1 in features] for f0 in features] for i in range(size)]
    index = features[0].index
    
    for z in range(size):
        t = m[z]
        for i in range(len(indexes)):
            for j in range(len(indexes)):
                if t[i][j]> 2.5:
                    print(f'{index[z]},{indexes[i]}-{indexes[j]}:{t[i][j]}, next day { [l[i][j] for l in m[z+1:z+5]]}')

#     result = list(zip(*t))
#     
#     print(len(result))
#     
    
    
    
    