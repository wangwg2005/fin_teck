import random
import json
import gym
from gym import spaces
import pandas as pd
import numpy as np

# MAX_ACCOUNT_BALANCE = 2147483647
# MAX_NUM_SHARES = 2147483647
# MAX_SHARE_PRICE = 5000
# MAX_OPEN_POSITIONS = 5
# MAX_STEPS = 20000

INITIAL_ACCOUNT_BALANCE = 10000
REWORD_INTERVAL=5

balance=0


class IndexEnv(gym.Env):
    """A stock trading environment for OpenAI gym"""
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(IndexEnv, self).__init__()


    def _nextObservation(self):
        
        self.currentPrice=random.randint(-1,1)
       

        return [self.currentPrice]

    def _takeAction(self, action):
        actionType = action[0]
#         amount = action[1]
#         pass
        if actionType==1:
            self.balance+=self.currentPrice;
        elif actionType==-1:
            self.balance-=self.currentPrice

    def step(self, action):
        # Execute one time step within the environment
        self._takeAction(action)

        self.currentStep += 1



        reward = self.currentPrice
        done = False

        obs = self._nextObservation()

        return obs, reward, done, {}

    def reset(self):
        # Reset the state of the environment to an initial state

        # Set the current step to a random point within the data frame
#         self.currentStep = random.randint(
#             0, len(self.df.loc[:, 'Open'].values) - 6)
        self.currentStep=0
        self.balance=0
        print("index env reset")

        return self._nextObservation()

    def render(self, mode='human', close=False):
        return np.array([1,1,1])
        # Render the environment to the screen
#         currentPrice = self.df.loc[self.currentStep, "Open"]
#         netWorth = self.balance + self.sharesHeld * currentPrice
#         profit = netWorth - INITIAL_ACCOUNT_BALANCE

#         print(f'Step: {self.currentStep}')
#         print(f'Balance: {self.balance}')
#         print(
#             f'Shares held: {self.sharesHeld} (Total sold: {self.totalSharesSold})')
#         print(
#             f'Avg cost for held shares: {self.averageShareCost} (Total sales value: {self.totalSalesValue})')
#         print(f'Net worth: {netWorth} (Max net worth: {self.maxNetWorth})')
#         print(f'Profit: {profit}')
