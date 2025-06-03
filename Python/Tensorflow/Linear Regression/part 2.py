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
        self.weight = tf.Variable(10.0) #m
        self.bias = tf.Variable(10.0) #b
        
    def __call__(self, x):
        return (self.weight * x) + self.bias

m = Model()
m(5)