# -*- coding: utf-8 -*-


import matplotlib.pyplot as plt
import pandas as pd
import datetime
import numpy as np
import file_cache as fc

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号


class Hmm:

    def __init__(self, df, circle=10):
        self.df = df
        self.circle=circle
        self.mask = 1

    def prepare_model(self):

        csi500 = self.df

        # csi500 = pd.read_csv("study\\history\\000905_20210131.csv", encoding="gbk")
        # csi500 = fc.get_from_cache("csi500")
        csi500.index = pd.to_datetime(csi500.pop("日期"), format='%Y-%m-%d')
        csi500 = csi500.sort_index()
        csi500 = csi500[["收盘价","涨跌幅"]]

#         csi500["涨跌幅1"] = csi500["收盘价"].diff() / csi500["收盘价"]
        csi500["涨跌"] = csi500["涨跌幅"].apply(lambda a: np.sign(float(a)))

        hash_vals = []
        hash = 0
        mask = (1 << self.circle) - 1
        for val in csi500["涨跌"].tolist():

            hash_vals.append(hash)
            hash = int(hash << 1)
            hash = (hash | int((val+1))>>1) & mask

        csi500["hash"] = hash_vals
        self.model=csi500

    def predict(self, pattern):
        m = self.model
        f = m[m["hash"] == pattern]
        if len(f)==0:
            print("no pattern found for",pattern)
            pos = self.circle
            p2= (pattern + (1 << (pos-1))) & ((1<<self.circle )-1)
            f = m[m["hash"] == pattern]
            if len(f)==0:
                print("2no has found for ",p2 )
#             while pos>0:
#                 pos-=1
                
            return 0
        
        
        cnt=f["涨跌"].sum()
        size=len(f)
#         if cnt== 0 :
#             return -f["涨跌幅"].mean()
#         else:
        return cnt
    
    def history(self, pattern, size=5):
        m = self.model
        f = m[m["hash"] == pattern]
        if len(f)==0:
            print("no pattern found for",pattern)
            return
        
        for ind in f.index:
            s = m[ind:][:10]["涨跌幅"].tolist()
            print(s)
            val=1
            vals=[1]
            for inc in s:
                val=val*(1+inc/100)
                vals.append(val)
            plt.plot(vals, label = str(ind)[:10])
            print("increament:",val-1)
        plt.show()
#         valiti_list=f["涨跌"].tolist()
#         return valiti_list.count(True)-valiti_list.count(False)
    
    def __str__(self):
        return str(self.model)
    
    def get_model(self):
        return self.model
    
    def compute_next(self,pattern,updown):
        mask=(1<<self.circle) - 1
        return ((pattern<<1) | updown)& mask
    
    def plot_by_ratio(self,a):
        print(a)
        val=1
        vals=[1]
        for inc in a:
           val=val*(1+inc/100)
           vals.append(val)
        print("increament:",val-1)
        plt.plot(vals, label = "real")


def test():
    csi500 = pd.read_csv("000905.csv", encoding="gbk")
    hist_model = Hmm(csi500)
    hist_model.prepare_model()
    
    recent = pd.read_csv("000905_20210131.csv", encoding="gbk")[:40]
    rece_model = Hmm(recent)
    rece_model.prepare_model()
    train_data=rece_model.get_model()
#     print(train_data)
    
    correct = 0
    wrong = 0
    
    for ind, row in train_data.iterrows():
        hash = row["hash"]
#         print(row)
        result=-hist_model.predict(hash)
        
        result_str=result>0
        t=result*row["涨跌"]
        if t>0:
            correct+=1
        elif t<0:
            wrong+=1
        print(ind," predict:",result," real:",row["涨跌"])
        
    print("correct:",correct)
    print("wrong",wrong)
    print("total:",len(train_data))
    
    
def predict():
    csi500 = pd.read_csv("000905.csv", encoding="gbk")
    hist_model = Hmm(csi500)
    hist_model.prepare_model()
    
    current=fc.get_from_cache("csi500")
      
    current=current.rename({"中证500":"收盘价"},axis='columns')
    current.index = pd.to_datetime(current["日期"], format='%Y-%m-%d')
    current = current.sort_index()
    current["涨跌幅"]=current["收盘价"].diff()/current["收盘价"]*100
    current_model=Hmm(current[1:])
    current_model.prepare_model()
    print(current_model.get_model())
    
    hist_model.plot_by_ratio(current[-8:]["涨跌幅"].tolist())
    hist_model.history(756)
    
#     print(current)
predict()
    
#     print(recent)
# test()
# for ind in len(range(inflow):

