# -*- coding: utf-8 -*-

import numpy as np
import matplotlib as plt
import pandas as pd


class Liner_model:
    def __init__(self,a,b):
        self.a=a
        self.b=b
        
    def predict(self,x):
        return self.a*x+self.b

csi500=Liner_model(1.10020619, 3132.59399)

def train_model(x, y, level=1):
    P=np.polyfit(x,y,level)
    print("model param",P)
    return (Liner_model(P[0],P[1]),np.polyval(P, x))

