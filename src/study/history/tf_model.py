# -*- coding: utf-8 -*-


import study.history.stock_vol_lev as sl
import numpy as np
from functools import reduce
import os
import pandas as pd

def feature(sid):

    f_orig = sl.get_f(sid)

    fn = f_orig[['incre']]
#     fn['Y']= fn['incre']*10


#     fn['lev_b_chg']=f_orig['lev_buy'].pct_change()
#     fn['lev_s_chg']=f_orig['lev_sell'].pct_change()
#     fn['vol_chg']=f_orig['volume'].pct_change()

    fn['lev_b_chg']=f_orig['lev_buy'].diff()
    fn['lev_s_chg']=f_orig['lev_sell'].diff()
    fn['vol_chg']=f_orig['volume'].diff()



    fn['low_min'] = f_orig['low'].shift(-1).rolling(window=10).min()
    fn['high_max'] = f_orig['high'].rolling(10).max().shift(-10)
    fn['Y'] = fn['incre'].rolling(window=10).max()*10
    fn['postive_return']=fn['high_max']/f_orig['close']-1
    
    fn['negtive_return']=fn['low_min']/f_orig['close']-1
    
    return fn.dropna()




# whole feature dataframe
def feature_enginering(df):
    df['lev_ratio']=2*df['rzmr']/((df['high']+df['low'])*df['volume'])
    df['high_max'] = df['high'].rolling(window=10).max().shift(-10)
    
    
    df['pre_close']=df['close'].shift()
    
    width= 7
    df['postive_return']=df['high_max']/df['open']-1
    df['chg1']=df['close']/df['open']-1
    df['chg']=df['close'].pct_change()
    df['chg_max']=df['chg'].map(lambda v: v if v>0 else -v).rolling(width,closed="left").max()
    
    df['vol_chg'] = df['volume'].pct_change().shift()
    df['vol_chg_max']=df['vol_chg'].map(lambda v: v if v>0 else -v).rolling(width,closed="left").max()
    df['vol_chg_comp']= df['vol_chg']/df['vol_chg_max']

    return df
#     width= 5
#     
#     num = len(df) - width +1
#     
#     fs = list(map(lambda ind:df[ind: ind+width],list(range(num))))
#     
#     return fs
    
    
# sperate data frame, one frame a day    
def bussniess_logic(df):
#     ratio = df['lev_ratio'].quantile(0.99)
#     if df['lev_ratio'].iat[-3]<ratio:
#         return False
    if df.iloc[-1]['open'] >= df.iloc[-2]['close']:
        return False
    
    if df.iloc[-2]['volume']<df.iloc[-3]['volume']*1.2:
        return False
    
from datetime import date

today = str(date.today())
# today = "2022-06-06"

print("today is "+today)

model_b_sids=[]



def model_d(sid,df):
#     df = df[:today]
#     print(df.columns)
    
    s = df['volume'].pct_change()
    
    s1 = s.gt(0)
    s2 = s.lt(0)
    
    df['vol_chg']=s
    df['vol_increase'] = s1.cumsum().where(s1, 0)
    df['vol_decrease'] = s2.cumsum().where(s2, 0)

    
    si = df['vol_increase'].eq(0)
    sd = df['vol_decrease'].eq(0)
    
    df['vol_inc'] = si.groupby(si.cumsum()).cumcount()
    df['vol_dec'] = sd.groupby(sd.cumsum()).cumcount()
    df['vol_colsum']= df.apply(lambda r: -r[-1] if r[-1]>0 else r[-2],axis=1)
    
    s=df['close'].pct_change()
    
    s1 = s.gt(0)
    s2 = s.lt(0)
    
    df['close_chg']=s
    df['close_increase'] = s1.cumsum().where(s1, 0)
    df['close_decrease'] = s2.cumsum().where(s2, 0)
    
    si = df['close_increase'].eq(0)
    sd = df['close_decrease'].eq(0)
    
    df['close_inc'] = si.groupby(si.cumsum()).cumcount()
    df['close_dec'] = sd.groupby(sd.cumsum()).cumcount()
    df['close_colsum']= df.apply(lambda r: -r[-1] if r[-1]>0 else r[-2],axis=1)
    
    df['high_max'] = df['high'].rolling(window=10).max().shift(-10)
    #df['vol_chg'] = df['vol_chg'].shift()
    df['positive_return']=df['high_max']/df['open']-1
    
    f=df[(df.vol_colsum>=5) | (df.vol_colsum<=-5)]

    print(df.index[-1])
#     print(df.columns)
    if len(f)>0 and  df.index[-1]==f.index[-1]:
        print("candidate id:"+sid)
        fpath = f"../../javascript/js/data/d_data_{today}.js";
        t = os.path.exists(fpath)
            
        with open(fpath,'a') as fo:
            obj = df[["vol_colsum","close_colsum","vol_chg","close_chg"]].iloc[-1]
            obj['sid'] = sid;
            obj=obj.to_json();
            if t:
                fo.write(f'model_data.d["{sid}"]={obj};\n')
            else:
                fo.write("model_data.d={'"+sid+"':"+obj+"};\n")
    
#     print(f)
    f.to_csv(os.path.join('data',sid+"_d.csv"))
#     f.to_csv(os.path.join('data',sid+"_b_quantile.csv"))
    return f['positive_return'].describe()



def model_c(sid,df):

#     df = df[:today]
#     print(df.columns)
    
    df['pre_open'] =df['open'].shift()
    df['pre_close']=df['close'].shift()
    df['vol_chg']=df['volume'].pct_change()
#     print(df.columns)
    
    df['down']= df.apply(lambda r: 1 if (r[0]<r[5] and r[3]< r[6]) else 0,axis=1)
    df['down_cnt'] = df['down'].rolling(window=3).sum()
    

    df['volatility'] = df['volume'].rolling(5).std()
    df['vol_0.1']= df['volatility'].rolling(30).quantile(0.1)
    df['vol_test'] = df.apply(lambda r : r[-2]<r[-1] ,axis=1)
    
    df['vol_test'] = df['vol_test'].shift(1)
    df['down_cnt'] = df['down_cnt'].shift()
    df['high_max'] = df['high'].rolling(window=10).max().shift(-10)
    #df['vol_chg'] = df['vol_chg'].shift()
    df['positive_return']=df['high_max']/df['open']-1
    
    f=df[(df.vol_test) &(df.vol_chg>0.5)]

    print(df.index[-1])
#     print(df.columns)
    if len(f)>0 and  df.index[-1]==f.index[-1]:
        print("candidate id:"+sid)
        fpath = f"../../javascript/js/data/c_sids_{today}.js";
        t = os.path.exists(fpath)
            
        with open(fpath,'a') as fo:
            if t:
                fo.write(f'mc_sids.push("{sid}");\n')
            else:
                fo.write(f'var mc_sids=["{sid}"];\n')
    
#     print(f)
    f.to_csv(os.path.join('data',sid+"_c.csv"))
#     f.to_csv(os.path.join('data',sid+"_b_quantile.csv"))
    return f['positive_return'].describe()
    
def model_b(sid):
    print("processing "+sid)
#     df = sl.get_f(sid, 0);
    df = pd.read_csv(os.path.join("stock",sid,"price.csv"),index_col=0,parse_dates=True)
#     df = df[:today]
#     print(df.columns)
    
    df['pre_open'] =df['open'].shift()
    df['pre_close']=df['close'].shift()
    
#     print(df.columns)
    
    df['down']= df.apply(lambda r: 1 if (r[0]<r[5] and r[3]< r[6]) else 0,axis=1)
    df['down_cnt'] = df['down'].rolling(window=3).sum()
    df['vol_chg']=df['volume'].pct_change()
    df['quant']=df['close'].rolling(30).quantile(.2)
    
    df['down_cnt'] = df['down_cnt'].shift()
    df['high_max'] = df['high'].rolling(window=10).max().shift(-10)
 #   df['vol_chg'] = df['vol_chg'].shift()
    df['positive_return']=df['high_max']/df['open']-1
    
    

    
    
    
    #     df.to_csv(os.path.join('data',sid+"_tmp.csv"))
#     print(df[['down','down_cnt']])
    

    f = df[(df.down_cnt==3) & (df.vol_chg>0.2)]
#     f = df[(df.down_cnt==3) & (df.vol_chg>0.2) &(df.close< df.quant)]
    

#     print(df.index[-1])
#     print(df.columns)
    if len(f)>0 and  df.index[-1]==f.index[-1]:
        print("candidate id:"+sid)
        fpath = f"../../javascript/js/data/b_sids_{today}.js";
        t = os.path.exists(fpath)
            
        with open(fpath,'a') as fo:
            if t:
                fo.write(f'mb_sids.push("{sid}");\n')
            else:
                fo.write(f'var mb_sids=["{sid}"];\n')
    
#     print(f)
    f.to_csv(os.path.join('data',sid+"_b.csv"))
#     f.to_csv(os.path.join('data',sid+"_b_quantile.csv"))
    return f['positive_return'].describe()
        
def model_a(sid):
    df = sl.get_f(sid, 0);
    
    lev_window = 30
    df['lev_ratio']=2*df['rzmr']/((df['high']+df['low'])*df['volume'])
    df["lev_ratio_max"]=df['lev_ratio'].rolling(window=lev_window).max()
    df['lev_ratio_is_max']=df['lev_ratio']==df['lev_ratio_max']
#     df['lev_ratio_is_max']=df['lev_ratio_is_max'].map(lambda b: 1 if b else 0).rolling(3).max()
    df['lev_ratio_is_max']=df['lev_ratio_is_max'].map(lambda b: 1 if b else 0)
#     df['lev_ration_max_exist']=df['lev_ratio_is_max'].
    
    df['high_max'] = df['high'].rolling(window=20).max()
    df['positive_return']=df['high_max']/df['open']-1
    
    df['vol_chg'] = df['volume'].pct_change()
    
    df['vol_chg']=df['vol_chg'].shift()
    df['lev_ratio_is_max']=df['lev_ratio_is_max'].shift(2)
    df['positive_return']=df['positive_return'].shift(-20)
    
    
    
    f = df[(df.lev_ratio_is_max ==1) & (df.vol_chg>0.2) ]
    f.to_csv(os.path.join('data',sid+"a.csv"))
    return f['positive_return'].describe()
    
    
    
def validate(sid='600333'):
    df = sl.get_f(sid,0)
    f0 = feature_enginering(df)
#     f1 = f0[(f0.vol_chg>0.2) & (f0.vol_chg_max<0.2)]  #002118 vol_chg_max<0.185
    f1 = f0[(f0.vol_chg> 2*f0.vol_chg_max) & (f0.chg>0) & (f0.chg1>0)]
    
    f1.to_csv(os.path.join('data',sid+".csv"))
    return f1['postive_return'].describe()
    

def train():
    import tensorflow as tf
    from tensorflow import keras
    f = feature('002118')
    print(f[["postive_return","negtive_return"]].values)
    print(f.columns)
    thredhold = 0.1
    f['return'] = f.apply(lambda r: 1 if r[7]>thredhold else -1 if r[8]< -thredhold else 0, axis=1)
    pr = f.pop("postive_return")
    nr = f.pop("negtive_return")
    f.pop("low_min")
    f.pop('Y')
    f.pop('incre')
    print(f.head(10))
    
    split_date='2019-12-31'
    train_dataset = f[:split_date]
    train_len = len(train_dataset)
    
    
    
    width = 30
    b=f.values
    datas = np.array(list(map(lambda i: b[i:i+width] , range(len(f)-width +1))))
    
    

    print(f'data length:{datas.shape}')
    
    
    ret = f.pop('return')[width-1:]

    labels = ret.map(lambda r: r+1).values
#     labels = tf.one_hot(labels,depth=3)
#     labels = f.pop('return')[width-1:].map(lambda r: 1 if r >0 else 0).values
    print(labels)
    print(f'label length:{len(labels)}')
    
    batch_size=8
    
    trainset = tf.data.Dataset.from_tensor_slices((datas[:train_len], labels[:train_len])).batch(batch_size)    
    
#     for f , l in trainset.take(2):
#         print(f)
#         print(l)
    
    validset = tf.data.Dataset.from_tensor_slices((datas[train_len:], labels[train_len:])).batch(batch_size)
#     print(trainset.take(1))
    model = tf.keras.models.Sequential([
#       tf.keras.Input(shape=(8,)),
#       tf.keras.layers.
      tf.keras.layers.Conv1D(32,5, activation='relu', input_shape=(30,5),padding='SAME'),
      tf.keras.layers.MaxPooling1D(3),
      tf.keras.layers.Conv1D(32,5, activation='relu', input_shape=(30,5),padding='SAME'),
      tf.keras.layers.MaxPooling1D(3),
      tf.keras.layers.Conv1D(32,5, activation='relu', input_shape=(30,5),padding='SAME'),
      tf.keras.layers.MaxPooling1D(3),
      tf.keras.layers.Flatten(),
      tf.keras.layers.Dense(16, activation='tanh'),

      tf.keras.layers.Dense(3, activation='sigmoid')
    ])
#    

#     sgd = optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True) 
    adam = keras.optimizers.Adam(lr=0.00001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)
    
    model.compile(optimizer=adam,
              loss='sparse_categorical_crossentropy',
              metrics=['sparse_categorical_accuracy'])
    
    model.fit(trainset, epochs=15)
    
    model.evaluate(validset,verbose=2)
    
    pred = model.predict(datas[train_len:])
    print(pred)
    
    print(ret)
    print(np.argmax(pred,axis=1))
    
    
# train()
if __name__ == '__main__':
    
    mv = pd.read_excel(os.path.join("data","market_value.xls"),index_col=1);
#     print(mv)
    
    records={}
#     models = [model_c,model_d]
    models = [model_d]
    for model in models:
        records[model.__name__]=[]
    
    sids = os.listdir("stock")
    sids = list(filter(lambda sid :sid<'010' or (sid>'600' and sid<'680'),sids))
    
    
    
    mvs= list(map(lambda sid: mv.loc[int(sid),'总市值']/100000000,sids))
    mvs1= list(map(lambda sid: mv.loc[int(sid),'流通市值']/100000000,sids))
#     print(mvs)

    sids = list(filter(lambda sid: sid[0] in ['0','6'],sids))
    price_dfs = map(lambda sid:pd.read_csv(os.path.join("stock",sid,"price.csv"),index_col=0,parse_dates=True), sids)
    for sid, df in zip(sids, price_dfs):
        for model in models:
            records[model.__name__].append(model.__call__(sid,df))
            
    for model in models:
        df = pd.DataFrame(records[model.__name__],index= sids)
        df['总市值']=mvs
        df['流通市值']=mvs1
        df.to_csv(os.path.join('data',f'{model.__name__}[-1]_desc_{today}.csv'))
    

