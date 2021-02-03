# -*- coding: utf-8 -*-


import matplotlib.pyplot as plt
import pandas as pd
import datetime

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号


class Hmm:

    def __init__(self, df):
        self.df = df

    def prepare_model(self):

        csi500 = self.df

        # csi500 = pd.read_csv("study\\history\\000905_20210131.csv", encoding="gbk")
        # csi500 = fc.get_from_cache("csi500")
        csi500.index = pd.to_datetime(csi500.pop("日期"), format='%Y-%m-%d')
        csi500 = csi500.sort_index()
        csi500 = csi500[["收盘价"]]

        csi500["涨跌幅"] = csi500["收盘价"].diff() / csi500["收盘价"]
        csi500["涨跌"] = csi500["收盘价"].diff() > 0

        hash_vals = []
        hash = 0
        mask = (1 << 10) - 1
        print(bin(mask))
        for val in csi500["涨跌"].tolist():

            hash_vals.append(hash)
            hash = int(hash << 1)
            hash = (hash | int(val)) & mask

        csi500["hash"] = hash_vals

    def predict(self, pattern):
        model = self.df
        f = model[model["hash"] == pattern]
        return f["涨跌幅"].mean()


def test():
    csi500 = pd.read_csv("study\\history\\000905_20210131.csv", encoding="gbk")
    hist_model = Hmm(csi500)



# for ind in len(range(inflow):

