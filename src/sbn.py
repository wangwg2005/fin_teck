# -*- coding: utf-8 -*-

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# mean,cov=[0,1],[(1,.5),(.5,1)]
# data=np.random.multivariate_normal(mean,cov,200)
# df=pd.DataFrame(data,columns=["x","y"])

x=[1,2,3]
y=[2,3,4]

sns.jointplot(x=x,y=y)
plt.savefig(r"C:\Users\Darren\eclipse-workspace\fin_study\src\study\leverage\img\demo.png")



