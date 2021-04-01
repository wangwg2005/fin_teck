# -*- coding: utf-8 -*-
import time
import pandas as pd

'''
Created on 2021��3��30��

@author: Darren
'''

import gym
import pandas


df=pd.DataFrame()

env = gym.make('IndexEnv-v0')
for i_episode in range(20):
    observation = env.reset()
    for t in range(100):
        env.render()
        
        observation, reward, done, info = env.step([1])
        print(observation,reward)
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break
        time.sleep(0.2)      #每次等待0.2s
env.close()