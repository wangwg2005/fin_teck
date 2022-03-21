# -*- coding: UTF-8 -*- 

import pandas as pd
import mplfinance as mpf

df = pd.read_csv(r'C:\Users\Darren\eclipse-workspace\fin_study\src\study\history\stock\002118\price.csv',encoding='utf8');
df['std'] = df['volume'].rolling(5).std(ddof=0)
print(df.head())

df['std'].plot();
