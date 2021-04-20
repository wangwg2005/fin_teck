# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import math

def sigmod(x):
    return math.exp(math.tanh(x))

x = np.linspace(-10, 10)
y = list(map( math.tanh,x))
y2= list(map(sigmod,x))
plt.plot(x,y)
plt.plot(x,y2)
plt.show()