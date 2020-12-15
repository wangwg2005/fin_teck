# -*- coding: utf-8 -*-

import os
from datetime import datetime


import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import tensorflow as tf

def convertPrice(l):
    vs=l.split(",")
    return {"date":vs[0],"index":vs[1],"close":float(vs[3]),"open":float(vs[6])}

with open(r"C:\Users\Darren\eclipse-workspace\AnnounceSpider\src\study\eastmoney\000905_4.csv",'r') as f:
    lines=f.readlines()


items=list(map(convertPrice,lines[1:]))
items.reverse()
items=items[2700:]
# items=items[:3600]
print("days:",len(items))
# ind_ts=list(map(lambda a: datetime.strptime(a["date"], "%Y-%m-%d"),items))

df=pd.DataFrame(items)

# csi300=pd.read_csv(r"C:\Users\Darren\eclipse-workspace\AnnounceSpider\src\study\eastmoney\000300_etled.csv",'r')

df.pop("index")
date_time = pd.to_datetime(df.pop('date'), format='%Y-%m-%d')
print(date_time)
df.index=date_time
df.plot(subplots=True)
# dff=df[["close","open"]]
# dff.index=date_time
# print("")
# print(dff)
# _ = dff.plot(subplots=True)
prices=list(map(lambda a:a["close"],items))
# 
# 
# plt.plot(prices)
# 

day_per_year = 365.2524
fft = tf.signal.rfft(prices)
f_per_dataset = np.arange(0, len(fft))
n_samples_h=len(items)
years_per_dataset = n_samples_h/day_per_year
f_per_year=f_per_dataset/years_per_dataset
# plt.step(f_per_dataset,np.abs(fft))
# plt.xscale('log')
# plt.xticks([1, 365.2524], labels=['1/Year', '1/day'])
# _ = plt.xlabel('Frequency (log scale)')
# # 


n = len(df)
train_df = df[0:int(n*0.7)]
val_df = df[int(n*0.7):int(n*0.9)]
test_df = df[int(n*0.9):]

print("np array")
print(np.array(train_df))


num_features = df.shape[1]
print("features",num_features)
#normalize
train_mean = train_df.mean()
print(train_mean)
train_std = train_df.std()
print(train_df)
train_df = (train_df - train_mean) / train_std
val_df = (val_df - train_mean) / train_std
test_df = (test_df - train_mean) / train_std


df_std = (df - train_mean) / train_std
# df_std = df_std.melt(var_name='Column', value_name='Normalized')
# plt.figure(figsize=(12, 6))
# ax = sns.violinplot(x='Column', y='Normalized', data=df_std)
# _ = ax.set_xticklabels(df.keys(), rotation=90)
# train_val=df["close"].values
# train_origin=train_val.copy()
# print(train_val)
# EMA = train_val[0]
# gamma = 0.1
# for ti in range(3600):
#  EMA = gamma*train_val[ti] + (1-gamma)*EMA
#  train_val[ti] = EMA
#  
# print(train_val)
# abc=tf.keras.utils.normalize(train_val, axis=-1, order=2)
# print(abc)
# plt.plot(train_origin)
# plt.plot(train_val)


column_indices = {name: i for i, name in enumerate(df.columns)}

class WindowGenerator():
    def __init__(self, input_width, label_width, shift,
               train_df=train_df, val_df=val_df, test_df=test_df,
               label_columns=None):
      # Store the raw data.
        self.train_df = train_df
        self.val_df = val_df
        self.test_df = test_df
    
        # Work out the label column indices.
        self.label_columns = label_columns
        if label_columns is not None:
          self.label_columns_indices = {name: i for i, name in
                                        enumerate(label_columns)}
        self.column_indices = {name: i for i, name in
                               enumerate(train_df.columns)}
    
        # Work out the window parameters.
        self.input_width = input_width
        self.label_width = label_width
        self.shift = shift
    
        self.total_window_size = input_width + shift
    
        self.input_slice = slice(0, input_width)
        self.input_indices = np.arange(self.total_window_size)[self.input_slice]
    
        self.label_start = self.total_window_size - self.label_width
        self.labels_slice = slice(self.label_start, None)
        self.label_indices = np.arange(self.total_window_size)[self.labels_slice]

    def __repr__(self):
        return '\n'.join([
            f'Total window size: {self.total_window_size}',
            f'Input indices: {self.input_indices}',
            f'Label indices: {self.label_indices}',
            f'Label column name(s): {self.label_columns}'])
        
        
def split_window(self, features):
  inputs = features[:, self.input_slice, :]
  labels = features[:, self.labels_slice, :]
  if self.label_columns is not None:
    labels = tf.stack(
        [labels[:, :, self.column_indices[name]] for name in self.label_columns],
        axis=-1)

  # Slicing doesn't preserve static shape information, so set the shapes
  # manually. This way the `tf.data.Datasets` are easier to inspect.
  inputs.set_shape([None, self.input_width, None])
  labels.set_shape([None, self.label_width, None])

  return inputs, labels

WindowGenerator.split_window = split_window
# all_mid_data = np.concatenate([train_data,test_data],axis=0)

# You normalize the last bit of remaining data 



def plot(self, model=None, plot_col='close', max_subplots=3):
  inputs, labels = self.example
  plt.figure(figsize=(12, 8))
  plot_col_index = self.column_indices[plot_col]
  max_n = min(max_subplots, len(inputs))
  for n in range(max_n):
    plt.subplot(3, 1, n+1)
    plt.ylabel(f'{plot_col} [normed]')
    plt.plot(self.input_indices, inputs[n, :, plot_col_index],
             label='Inputs', marker='.', zorder=-10)

    if self.label_columns:
      label_col_index = self.label_columns_indices.get(plot_col, None)
    else:
      label_col_index = plot_col_index

    if label_col_index is None:
      continue

    plt.scatter(self.label_indices, labels[n, :, label_col_index],
                edgecolors='k', label='Labels', c='#2ca02c', s=64)
    if model is not None:
      predictions = model(inputs)
      plt.scatter(self.label_indices, predictions[n, :, label_col_index],
                  marker='X', edgecolors='k', label='Predictions',
                  c='#ff7f0e', s=64)

    if n == 0:
      plt.legend()

  plt.xlabel('Time [trade day]')

WindowGenerator.plot = plot

def make_dataset(self, data):
  data = np.array(data, dtype=np.float32)
  ds = tf.keras.preprocessing.timeseries_dataset_from_array(
      data=data,
      targets=None,
      sequence_length=self.total_window_size,
      sequence_stride=1,
      shuffle=True,
      batch_size=32,)

  ds = ds.map(self.split_window)

  return ds

WindowGenerator.make_dataset = make_dataset

@property
def train(self):
  return self.make_dataset(self.train_df)

@property
def val(self):
  return self.make_dataset(self.val_df)

@property
def test(self):
  return self.make_dataset(self.test_df)

@property
def example(self):
  """Get and cache an example batch of `inputs, labels` for plotting."""
  result = getattr(self, '_example', None)
  if result is None:
    # No example batch was found, so get one from the `.train` dataset
    result = next(iter(self.train))
    # And cache it for next time
    self._example = result
  return result

WindowGenerator.train = train
WindowGenerator.val = val
WindowGenerator.test = test
WindowGenerator.example = example

w2 = WindowGenerator(input_width=6, label_width=1, shift=1,
                     label_columns=['close'])

print(w2)
print(w2.train.element_spec)

single_step_window = WindowGenerator(
    input_width=1, label_width=1, shift=1,
    label_columns=['close'])

for example_inputs, example_labels in single_step_window.train.take(1):
  print(f'Inputs shape (batch, time, features): {example_inputs.shape}')
  print(f'Labels shape (batch, time, features): {example_labels.shape}')
  
  
  


wide_window = WindowGenerator(
    input_width=24, label_width=24, shift=1,
    label_columns=['close'])

# print(wide_window)
# wide_window.plot()


MAX_EPOCHS = 20

def compile_and_fit(model, window, patience=2):
  early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss',
                                                    patience=patience,
                                                    mode='min')

  model.compile(loss=tf.losses.MeanSquaredError(),
                optimizer=tf.optimizers.Adam(),
                metrics=[tf.metrics.MeanAbsoluteError()])

  history = model.fit(window.train, epochs=MAX_EPOCHS,
                      validation_data=window.val,
                      callbacks=[early_stopping])
  return history

class Baseline(tf.keras.Model):
      def __init__(self, label_index=None):
        super().__init__()
        self.label_index = label_index
    
      def call(self, inputs):
        if self.label_index is None:
          return inputs
        result = inputs[:, :, self.label_index]
        return result[:, :, tf.newaxis]

def linear_mode():
    linear = tf.keras.Sequential([
        tf.keras.layers.Dense(units=1)
    ])
    
    history = compile_and_fit(linear, single_step_window)
    
    
    
    wide_window.plot(linear)

# baseline = Baseline(label_index=column_indices['close'])
# 
# baseline.compile(loss=tf.losses.MeanSquaredError(),
#                  metrics=[tf.metrics.MeanAbsoluteError()])
# 
val_performance = {}
performance = {}
# val_performance['Baseline'] = baseline.evaluate(single_step_window.val)
# performance['Baseline'] = baseline.evaluate(single_step_window.test, verbose=0)

def dense_mode():
  dense = tf.keras.Sequential([
    tf.keras.layers.Dense(units=64, activation='relu'),
    tf.keras.layers.Dense(units=64, activation='relu'),
    tf.keras.layers.Dense(units=1)
  ])
  
  history = compile_and_fit(dense, single_step_window)

  val_performance['Dense'] = dense.evaluate(single_step_window.val)
  performance['Dense'] = dense.evaluate(single_step_window.test, verbose=0)
  wide_window.plot(dense)
  
CONV_WIDTH = 3
conv_window = WindowGenerator(
    input_width=CONV_WIDTH,
    label_width=1,
    shift=1,
    label_columns=['close'])

print(conv_window)
conv_window.plot()

def multi_dense_mode():
    multi_step_dense = tf.keras.Sequential([
        # Shape: (time, features) => (time*features)
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(units=32, activation='relu'),
        tf.keras.layers.Dense(units=32, activation='relu'),
        tf.keras.layers.Dense(units=1),
        # Add back the time dimension.
        # Shape: (outputs) => (1, outputs)
        tf.keras.layers.Reshape([1, -1]),
    ])
    
OUT_STEPS = 24
multi_window = WindowGenerator(input_width=24,
                               label_width=OUT_STEPS,
                               shift=OUT_STEPS)

# multi_window.plot()
# print(multi_window)

class FeedBack(tf.keras.Model):
  def __init__(self, units, out_steps):
    super().__init__()
    self.out_steps = out_steps
    self.units = units
    self.lstm_cell = tf.keras.layers.LSTMCell(units)
    # Also wrap the LSTMCell in an RNN to simplify the `warmup` method.
    self.lstm_rnn = tf.keras.layers.RNN(self.lstm_cell, return_state=True)
    self.dense = tf.keras.layers.Dense(num_features)
    

def warmup(self, inputs):
  # inputs.shape => (batch, time, features)
  # x.shape => (batch, lstm_units)
  x, *state = self.lstm_rnn(inputs)

  # predictions.shape => (batch, features)
  prediction = self.dense(x)
  return prediction, state

FeedBack.warmup = warmup
    
feedback_model = FeedBack(units=32, out_steps=OUT_STEPS)   

prediction, state = feedback_model.warmup(multi_window.example[0])
print(prediction.shape)

def call(self, inputs, training=None):
  # Use a TensorArray to capture dynamically unrolled outputs.
  predictions = []
  # Initialize the lstm state
  prediction, state = self.warmup(inputs)

  # Insert the first prediction
  predictions.append(prediction)

  # Run the rest of the prediction steps
  for n in range(1, self.out_steps):
    # Use the last prediction as input.
    x = prediction
    # Execute one lstm step.
    x, state = self.lstm_cell(x, states=state,
                              training=training)
    # Convert the lstm output to a prediction.
    prediction = self.dense(x)
    # Add the prediction to the output
    predictions.append(prediction)

  # predictions.shape => (time, batch, features)
  predictions = tf.stack(predictions)
  # predictions.shape => (batch, time, features)
  predictions = tf.transpose(predictions, [1, 0, 2])
  return predictions

FeedBack.call = call


history = compile_and_fit(feedback_model, multi_window)
 
multi_val_performance={}
multi_performance={}
multi_val_performance['AR LSTM'] = feedback_model.evaluate(multi_window.val)
multi_performance['AR LSTM'] = feedback_model.evaluate(multi_window.test, verbose=0)
multi_window.plot(feedback_model)


# lstm_model = tf.keras.models.Sequential([
#     # Shape [batch, time, features] => [batch, time, lstm_units]
#     tf.keras.layers.LSTM(32, return_sequences=True),
#     # Shape => [batch, time, features]
#     tf.keras.layers.Dense(units=1)
# ])
# 
# history = compile_and_fit(lstm_model, wide_window)
# 
# # IPython.display.clear_output()
# val_performance['LSTM'] = lstm_model.evaluate(wide_window.val)
# performance['LSTM'] = lstm_model.evaluate(wide_window.test, verbose=0)
# wide_window.plot(lstm_model)

plt.show()