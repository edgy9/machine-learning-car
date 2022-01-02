
from self_drive3 import *
import tensorflow as tf
from tensorflow import keras

n_inputs = 6

model = keras.models.Sequential([
    keras.layers.Dense(5, activation="elu", input_shape=[n_inputs]),
    keras.layers.Dense(1,activation="sigmoid"),
])