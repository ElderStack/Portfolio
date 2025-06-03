import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0,4,100)
m = 2
b = 0.5
#y = m * x + b
y = m * x + b + np.random.randn(*x.shape) + 0.25


plt.scatter(x,y)
plt.show()

class Model:
    def __init__(self):
        #training is just changing these values
        #use .assign_sub(x) to change tf.Variable value
        self.weight = tf.Variable(10.0) #m
        self.bias = tf.Variable(10.0) #b
        
    def __call__(self, x):
        return (self.weight * x) + self.bias

def calculate_loss(y_actual, y_expected):
    #step 1: find loss -> y.act - y.exp
    #step 2: square to remove negative values
    #step 3: find mean
    return tf.reduce_mean(tf.square(y_actual - y_expected))

