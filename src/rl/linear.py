# -*- coding: utf-8 -*-

import numpy as np
np.random.seed(1337)  
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import matplotlib.pyplot as plt
 
# ��������
X = np.linspace(-1, 1, 200) #�ڷ��أ�-1, 1����Χ�ڵĵȲ�����
np.random.shuffle(X)    # ����˳��
Y = 0.5 * X + 2 + np.random.normal(0, 0.05, (200, )) #����Y���������
# plot
plt.scatter(X, Y)
plt.show()
 
X_train, Y_train = X[:160], Y[:160]     # ǰ160������Ϊѵ�����ݼ�
X_test, Y_test = X[160:], Y[160:]      #��40������Ϊ�������ݼ�
 
# ����������ģ��
model = Sequential()
model.add(Dense(input_dim=1, units=1))
 
# ѡ��loss�������Ż���
model.compile(loss='mse', optimizer='sgd')
 
# ѵ������
print('Training -----------')
for step in range(501):
    cost = model.train_on_batch(X_train, Y_train)
    if step % 50 == 0:
        print("After %d trainings, the cost: %f" % (step, cost))
 
# ���Թ���
print('\nTesting ------------')
cost = model.evaluate(X_test, Y_test, batch_size=40)
print('test cost:', cost)
W, b = model.layers[0].get_weights()
print('Weights=', W, '\nbiases=', b)
 
# ��ѵ��������
Y_pred = model.predict(X_test)
plt.scatter(X_test, Y_test)
plt.plot(X_test, Y_pred)
plt.show()