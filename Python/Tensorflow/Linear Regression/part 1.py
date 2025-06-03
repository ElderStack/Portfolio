#import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0,4,100)
m = 2
b = 0.5
#y = m * x + b
y = m * x + b + np.random.randn(*x.shape) + 0.25


plt.scatter(x,y)
plt.show()