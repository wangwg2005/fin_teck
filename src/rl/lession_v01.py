# -*- coding: utf-8 -*-
import time
import pandas as pd
from tensorflow.keras import models, layers, optimizers
import numpy as np
import math
import matplotlib.pyplot as plt

'''
Created on 2021年3月30日

@author: Darren
'''

import gym
import pandas


STATE_DIM, ACTION_DIM = 1, 3
model = models.Sequential([
    layers.Dense(32, input_shape=(None,3)),
#     layers.Dropout(0.1),
    layers.Dense(ACTION_DIM),
    layers.Dense(1,activation="tanh")
])
model.compile(loss='mean_squared_error',
              optimizer=optimizers.Adam(0.001))


def choose_action(s):
    """预测动作"""
    prob = model.predict(np.array([s]))[0]
#     prob=prob
#     print("prob",prob)
    return -round(prob[0])


def sample_weight(reward):
    
    return -reward*5+1


def train(records):
    s_batch = np.array([record[0] for record in records])
    # action 独热编码处理，方便求动作概率，即 prob_batch
    a_batch = np.array([[1 if record[1] == i else 0 for i in range(ACTION_DIM)]
                        for record in records])
    # 假设predict的概率是 [0.3, 0.7]，选择的动作是 [0, 1]
    # 则动作[0, 1]的概率等于 [0, 0.7] = [0.3, 0.7] * [0, 1]
    prob_batch = model.predict(s_batch) * a_batch
    r_batch = np.array([sample_weight(record[2]) for record in records])
    print(r_batch)
    model.fit(s_batch, prob_batch,sample_weight=r_batch,  verbose=0)
#     model.fit(s_batch, prob_batch,  verbose=0)

def target_feature(state):
    return [state["resid"]*5+0.5,state["chg1"],state["chg2"]]

df=pd.DataFrame()

env = gym.make('IndexEnv-v0')

score_list=[]

replay_df=pd.DataFrame()

for i_episode in range(20):
    state = env.reset()
    obs=target_feature(state)
    replay_records = []
    work=True
    reward_list=[]
    step=0
    while work:
        action=choose_action(obs)
#         print("obs:",obs,"action",action)
        
        state, reward, done, info = env.step([action])
#         if reward>0.1:
#             print("wrong reward：",reward)
        next_obs=target_feature(state)
        work= not done
#         if reward>-1:
        replay_records.append([obs,action,reward])
        
        reward_list.append(info["total"])
        step +=1
        obs=next_obs
        
    score=reward_list[-1]
    score_list.append(score)
    train(replay_records)
    profits=reward_list
    profits.append(profits[-1])
    
    env.features["profit"]=profits
#     env.features['profit']=env.features["profit"].cumprod()
    
    replay_df["episode"+str(i_episode)]=list(env.features['profit'])
    print('episode:', i_episode, 'score:',score , 'max:', max(score_list))
    env.features[["收盘价","profit"]].plot(grid=True,subplots=True)
    f=plt.savefig(r"C:\Users\Darren\Documents\rl\episode{0}.png".format(i_episode))
    plt.close(f)

plt.plot(score_list)
plt.savefig(r"C:\Users\Darren\Documents\rl\episode.png")
plt.show()
env.close()

