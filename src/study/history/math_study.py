# -*- coding: utf-8 -*-

import pandas as pd

csi500=pd.read_csv("000905.csv",encoding="gbk")

csi500=csi500[:60]
csi500.reindex(index=csi500.index[::-1])

print(csi500[["日期","收盘价"]])