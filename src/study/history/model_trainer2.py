# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from scipy import stats


from sklearn.linear_model import LinearRegression
import statsmodels.api as sm

trade_days=1000

def read_history(fname):
    df=pd.read_csv(fname,encoding="utf8",parse_dates=[0],index_col=0)
    return df

def read_leverage(fname):
    df = pd.read_excel(fname,header=1,parse_dates=[0],index_col=0)
    return df

def get_sub_set(df,start_date, end_date):
    return df[end_date:start_date]

### price file first , leverage data second
def read_dir(path):
    files = os.listdir( path );
    
    if files[0][-3:]=="csv":
        return files
    else :
        return (files[1],files[0])
    

def stream_model(root,sample_start="2020-01-02", sample_end="2020-12-31",pred_start="2021-01-02"):
    price_file, leverage_file=read_dir(root)
    
    price_df=read_history(os.path.join(root,price_file))
    f1=os.path.join(root,leverage_file)
    leve_df=read_leverage(f1)
    
    
    features=price_df[["收盘价","成交量"]]
    features.rename(columns={"收盘价":"price","成交量":"volumn"},inplace=True)
    features["lev"]=leve_df["融资余额(亿元)"]
    features.dropna(inplace=True)
    features.sort_index(inplace=True)
    
    train_data=features[sample_start:sample_end]
    print("train length",len(train_data))
    X=sm.add_constant(train_data[["lev"]])
    model=sm.OLS(train_data["price"],X).fit()
    print(model.summary())
    
    
    pred_df=features[pred_start:]
    print(len(pred_df["lev"]))
#     new_x=
    pred_df["pred"]=model.predict(sm.add_constant(pred_df[["lev"]]))
    pred_df["residual"]=pred_df["price"]-pred_df["pred"]
    pred_df["residual_norm_a"]=pred_df["residual"]/pred_df["pred"]
    
    window=20
    pred_df["residual_slide_std"]=pred_df["residual"].rolling(window).std()
    pred_df["residual_norm"]=pred_df["residual"]/pred_df["residual_slide_std"]
    pred_df[["residual","residual_norm","residual_norm_a","price"]].plot(subplots=True,grid=True)
    plt.show()
    
    
    
    
    
#     window=20
    
#     features["mean"]=features["收盘价"].rolling(window).mean()
#     features["std"]=features["收盘价"].rolling(window).std()
#     features["residual"]
    

    

def model1_train(root,train_start="2019-01-01", train_end="2020-12-31", his_start="2020-01-01", his_end=""):
    
#     features=csi500[["最高价","最低价","开盘价","收盘价"]]
#     print(features)
#     root="csi500"
    price_file, leverage_file=read_dir(root)
    
    csi500=read_history(os.path.join(root,price_file))
    f1=os.path.join(root,leverage_file)
    leve_csi500=read_leverage(f1)
    
    features=csi500[["收盘价","成交量"]]
    features["lev"]=leve_csi500["融资余额(亿元)"]
    features.dropna(inplace=True)
    
#     train_date=("2019-01-01","2020-12-31")
    
#     train_set=get_sub_set(features, *train_date)
    train_set=features[train_start:train_end]
    print(train_set)
    
    lr=LinearRegression()
#     X=np.array(train_set["lev"]).reshape(1, -1)
#     y=np.array(train_set["收盘价"]).reshape(1, -1)
    lr.fit(train_set[["lev"]], train_set["收盘价"])
    
    features["pred"]=lr.predict(features[["lev"]])
    features["resid"]=features["收盘价"]-features["pred"]
    features["resid_norm"]=features["resid"]/features["pred"]

#     features[:"2020-01-01"].plot(grid=True)
#     plt.show()
    features['成交量'] = features['成交量'].astype('float64')
    features=features[his_start:][["收盘价","resid","resid_norm"]]
    

    val=features["resid_norm"][0]
    print("val",val)
    

        
    msg = "{:.2f}".format(100-stats.percentileofscore(features["resid_norm"], val))+"%"
#     msg=" low than "+msg
    features.plot(grid=True,subplots=True,title=root+":"+msg)
    plt.savefig(r"C:\Users\Darren\eclipse-workspace\fin_study\src\study\leverage\img\z_score\old2_"+root+".png")
    plt.close()
     
    return msg, features
#     test_set["pred"]=lr.predict(np.array(test_set["lev"]).reshape(1, -1))

def old_train():
    names=["000905","000300","399006","000016"]
    # names=["000016"]
    data={}
    
    for name in names:
        percentile,features= model1_train(name)
        data[name+":"+percentile] = features["resid_norm"]
        
    df=pd.DataFrame(data)
    df.plot(grid=True,subplots=True)
    plt.savefig(r"C:\Users\Darren\eclipse-workspace\fin_study\src\study\leverage\img\z_score\summary2.png")
    
    plt.close()
    
if __name__=="__main__":    
    stream_model("000905")
#     test_set.plot(grid=True)

# 
# df=model1_train("csi500",his_start="2019-01-01")
# plt.show()
# df.to_csv(r"C:\Users\Darren\Documents\features.csv",encoding="utf8")

