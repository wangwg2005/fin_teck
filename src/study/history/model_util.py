# -*- coding: utf-8 -*-

import numpy as np
import matplotlib as plt
import pandas as pd


class liner_model:
    def __init__(self,a,b):
        self.a=a
        self.b=b
        
    def predict(self,x):
        return self.a*x+self.b


def train_model(x, y):
    P=np.polyfit(x,y,1)
    print("model param",P)
    return (liner_model(P[0],P[1]),np.polyval(P, x))

if __name__ == '__main__':
    
    xx=np.arange(10)
    yy=np.arange(1,20,2)
    print(xx)
    print(yy)
    model1=train_model(xx, yy)[0]
    print(model1.predict(5))