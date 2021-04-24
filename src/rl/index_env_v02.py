# -*- coding: utf-8 -*-

import random
import json
import gym
from gym import spaces
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


INITIAL_ACCOUNT_BALANCE = 100000
REWARD_INTERVAL=5

NO_FEE_DAYS=22

FEE_RATE=0.005


ONE_HAND=10000

MAX_PRETELL_DAYS=10
MIN_PRETELL_DAYS=5

CIRCLE=10


# this version , the amount trade each time is variable.


class IndexEnv(gym.Env):
    """A stock trading environment for OpenAI gym"""
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(IndexEnv, self).__init__()
        self.features=pd.read_csv(r"C:\Users\Darren\Documents\features.csv",encoding="utf8")
        close=self.features["收盘价"]
        self.features["incr"]=(close/close.shift(periods=-1))-1
#         self.features["chg"]=close.diff(period=-1)/close
        self.features.dropna(inplace=True)
        self.position=[]
        self.round=0
        self.asset_his=pd.DataFrame()


    def _nextObservation(self):
        
        row=self.features.loc[self.currentStep]
        
        start=max(self.currentStep-CIRCLE,0)
        
        end=max(self.currentStep-1,0)
        
        if end==0:
            chg1=0
            chg2=0
        else:
        
            chg1=self.features[start:end]["收盘价"].min()/self.currentPrice
            
            chg2=self.features[start:end]["收盘价"].max()/self.currentPrice
        
        return {"resid":row["resid"],"chg1":chg1,"chg2":chg2}
    
    def buy(self,amount):
        
        if self.balance<amount:
            return
    
        
        self.balance-=amount
        self.position.append({"date":self.currentStep,"price":self.currentPrice,"amount":amount})
        
        
    def sell(self,amount):
        
        rewards=[]
        
        cumu=amount
        
        while len(self.position)>0 and self.currentStep-self.position[0]["date"]>REWARD_INTERVAL:
            trade=self.position[0]
            
            trade_amount=0
            if trade["amount"]<=cumu:
                self.position.pop(0)
                cumu-=trade["amount"]
                trade_amount=trade["amount"]
            else:
                trade["amount"]-=cumu
                trade_amount=cumu
                
            
            fee_rate=0
            if self.currentStep-trade["date"]>NO_FEE_DAYS:
                fee_rate=0.005
                
                
            
            profit_rate=self.currentPrice/trade["price"]-fee_rate
            rewards.append((trade["date"],self.currentStep,profit_rate))
            
            # something left, logic not completed
            
            self.balance+=profit_rate*ONE_HAND
            
        return rewards
        
    def settle(self):
        
        market_value=0
        for trade in self.position:
            market_value+= self.currentPrice/trade["price"]*ONE_HAND
        
        settle_result={"balance":self.balance,"stock_value":market_value,"total":self.balance+market_value}
        self.asset_his=self.asset_his.append(settle_result, ignore_index=True)
        return settle_result
        

    def _takeAction(self, action):
        rewards=[]
        actionType = action[0]
        amount = action[1]*ONE_HAND
#         pass
        if actionType==0:
            return rewards
        
        df=self.features
        self.currentPrice=df.loc[self.currentStep]["收盘价"]
        end=min(self.currentStep+MAX_PRETELL_DAYS,len(df)-1)
        start=max(self.currentStep,end-MIN_PRETELL_DAYS)
        
        if actionType==1:
            
            self.buy(amount)
        
        elif actionType==-1:
            rewards= self.sell(amount) 
        
        
        return rewards
                    
#         elif actionType==-1:
#             self.balance-=self.currentPrice
        

    def step(self, action):
        # Execute one time step within the environment
        reward=self._takeAction(action)
        result=self.settle()
        self.currentStep += 1

        done = self.currentStep == len(self.features) -1

        obs = self._nextObservation()
        
        

        return obs, reward, done, result

    def reset(self):


        if len(self.asset_his)>0:
            self.asset_his.to_csv(r"C:\Users\Darren\Documents\rl\settle_{0}.csv".format([self.round]),encoding="utf8")
            ax=self.asset_his.plot(grid=True,subplots=True)
            
            plt.savefig(r"C:\Users\Darren\Documents\rl\settle_{0}.png".format([self.round]))

            plt.close()
        self.round+=1
        self.asset_his=pd.DataFrame(columns=["balance","stock_value","total"])
        self.currentStep=0
        self.balance=INITIAL_ACCOUNT_BALANCE
        self.delta=0
        self.currentPrice=0
        self.position=[]

        return self._nextObservation()

    def render(self, mode='human', close=False):
        return np.array([1,1,1])