# -*- coding: utf-8 -*-
import tensorflow as tf

import numpy as np


X_raw = np.array([2016, 2017, 2018, 2019, 2020], dtype=np.float32)
y_raw = np.array([20000, 23000, 27000, 32500, 47500], dtype=np.float32)

X = (X_raw - X_raw.min()) / (X_raw.max() - X_raw.min())
y = (y_raw - y_raw.min()) / (y_raw.max() - y_raw.min())


X = tf.constant(X)
y = tf.constant(y)

print("X",X)
print("Y",y)

a = tf.Variable(initial_value=0.)
b = tf.Variable(initial_value=0.)
variables = [a, b]

num_epoch = 10000  
optimizer = tf.keras.optimizers.SGD(learning_rate=5e-4)        
# 定义随机梯度下降法中的优化器和学习率
for e in range(num_epoch):
    # 使用tf.GradientTape()记录损失函数的梯度信息
    with tf.GradientTape() as tape:
        y_pred = a * X + b
        loss = tf.reduce_sum(tf.square(y_pred - y))
    # TensorFlow自动计算损失函数关于自变量（模型参数）的梯度
    grads = tape.gradient(loss, variables)
    # TensorFlow自动根据梯度更新参数
    optimizer.apply_gradients(grads_and_vars=zip(grads, variables))

print(a, b)