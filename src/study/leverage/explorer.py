# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import json
import numpy as np


def explore_detail():
    with open("detail_2019_now.json",'r') as f:
        detail=json.load(f)
    
    
    
    keys=list(detail.keys())
    for ind in range(len(detail)):
        ax=plt.subplot(2,2,ind+1)
        key=keys[ind]

        ax.plot(detail[key]["low"] ,label="high")
#         ax.plot(detail[key]["low"] , label="low")
#         ax.plot(detail[key]["close"],label="close")

#         high_mean=np.mean(detail[key]["high"])
#         low_mean=np.mean(detail[key]["low"])
#         close_mean=np.mean(detail[key]["close"])
#         plt.hist(np.array(detail[key]["high"])-high_mean, 100)
#         plt.hist(np.array(detail[key]["high"])-high_mean,50)
#         plt.hist(np.array(detail[key]["close"])-close_mean, 100)
        ax.set_title(key)
        ax.grid(True)
    plt.show()
    
    
explore_detail()