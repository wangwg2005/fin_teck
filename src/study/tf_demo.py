# -*- coding: utf-8 -*-

import numpy as np
import tensorflow as tf


data=np.array(100)
print(data)
ds = tf.keras.preprocessing.timeseries_dataset_from_array(
      data=data,
      sequence_length=10,  sampling_rate=2, sequence_stride=3,
    shuffle=False)

print(ds)