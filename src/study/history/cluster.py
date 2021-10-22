# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import pandas as pd
from study.history import model_trainer2 as mt
import os
from scipy import stats
import statsmodels.api as sm
import seaborn as sns
import numpy as np
from sklearn.cluster import DBSCAN 
import matplotlib.cm as cm 


indepent_var="融资融券余额(亿元)"


def get_df(name):
    files=list(map(lambda a:os.path.join(name,a),mt.read_dir(name)))
        
    start="2013-12-31"
    
    split_date="2020-12-31"
    
    prices=mt.read_history(files[0])[start:]
    
    lever=mt.read_leverage(files[1])[start:]
#     lever.plot()
#     plt.show()
    
    df=prices[["收盘价"]]
    df["lev"]=lever[indepent_var]
    df=df.rename(columns={"收盘价":"price"})
    df=df.dropna()
    df=df.sort_index()
#     return df[:split_date],df[split_date:]
    return df


def cluster_data(name):
    df=get_df(name)
    print(df)
    
#     X = df[["lev"]]
    X=df
    db = DBSCAN(eps=120, min_samples=10).fit(X)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    
    # Black removed and is used for noise instead.
    unique_labels = set(labels)
    colors = cm.Spectral(np.linspace(0, 1, len(unique_labels)))
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = 'k'
    
        class_member_mask = (labels == k)
    
        xy = X[class_member_mask & core_samples_mask]
#         print("xy",xy)
        plt.plot(xy["lev"], xy["price"], 'o', markerfacecolor=col,
                 markeredgecolor='k', markersize=14)
    
        xy = X[class_member_mask & ~core_samples_mask]
        plt.plot(xy["lev"], xy["price"], 'o', markerfacecolor=col,
                 markeredgecolor='k', markersize=6)
    
    plt.title('Estimated number of clusters: %d' % n_clusters_)
    plt.show() 
    
    
    
    
if __name__=="__main__":
    names=["000905","000300","399006","000016"]
    
    
    cluster_data("000905")
    
#     for name in names:
#          cluster_data(name)
#         print(get_coor(name))
#         print(name)


