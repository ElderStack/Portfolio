import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0,4,100)
m = 2
b = 0.5
#y = m * x + b
y = m * x + b + np.random.randn(*x.shape) + 0.25

# plt.scatter(x,y)
# plt.show()

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

def train (model, x, y_expected, learning_rate):
    with tf.GradientTape() as gt:
        y_output = model(x)
        loss = calculate_loss(y_output, y_expected)
        
        new_weight, new_bias = gt.gradient(loss, [model.weight, model.bias])
        model.weight.assign_sub(new_weight * learning_rate)
        model.bias.assign_sub(new_bias * learning_rate)
        
model = Model()
epochs = 100 #how many passes through the training function
learning_rate = 0.15
current_epochs = []
losses = []

for epoch in range(epochs):
    y_output = model(x)
    loss = calculate_loss(y_output, y)
    print(f"Epoch: {epoch}, loss: {loss.numpy()}")
    current_epochs.append(epoch)
    losses.append(loss)
    train(model, x, y, learning_rate)
    
# plt.plot(current_epochs, losses)
# plt.show()