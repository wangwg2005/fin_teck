# -*- coding: utf-8 -*-


import matplotlib.pyplot as plt
import pandas as pd
import file_cache as fc


def read(filename):
    df = pd.read_excel("融资融券"+filename+".xls",header=1, encoding="gbk")
    return df


recent=read("csi500_2021")
recent=recent.dropna()

date_time = pd.to_datetime(recent.pop('交易日期'), format='%Y-%m-%d')
recent.index=date_time

features=fc.get_from_cache("csi500")

print(features)