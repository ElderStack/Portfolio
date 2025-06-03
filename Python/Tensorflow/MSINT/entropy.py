import numpy as np
import tensorflow as tf
from tensorflow import keras
from matplotlib import pyplot as plt
import seaborn as sn

#y_train correpsonds to which number it is
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

#num of digits, arr len, arr width
# print(x_train.shape)
# print(x_test.shape)

#illustration shown as values
# print(*x_train[0])

#restrict data between 0 and 1
x_train = x_train / 255
x_test = x_test / 255

#illstrate data
# index = 0
# plt.imshow(x_train[index], cmap = plt.cm.binary)
# plt.show()

#flatten data into single array
x_train_flat = x_train.reshape(len(x_train), (28 * 28)) #28 pixels by 28 pixels
x_test_flat = x_test.reshape(len(x_test), (28 * 28))

#show new shape
#print(x_train_flat[0])


model = keras.Sequential([
    #Dense(# of neurons, shape of input, type of neuron)
    keras.layers.Dense(128, input_shape = (784,), activation = 'relu'), #relu(x) = max(0, x)
    keras.layers.Dense(64, activation = 'sigmoid'),
    keras.layers.Dense(32, activation = 'sigmoid'),
    keras.layers.Dense(10, activation = 'softmax'), #classification function, returns probability it belongs to a certain class
])

model.compile(
    optimizer = 'adam',
    loss = 'sparse_categorical_crossentropy',
    metrics = ['accuracy']
)

#running the model on training data
model.fit(x_train_flat, y_train, epochs = 5)

#testing the model
model.evaluate(x_test_flat, y_test)

#seeing where the model messed up
y_pred = model.predict(x_test_flat)
y_pred_labels = [np.argmax(i) for i in y_pred]

confusion_matrix = tf.math.confusion_matrix(labels = y_test, predictions = y_pred_labels)
sn.heatmap(confusion_matrix, annot = True, fmt = 'd')
plt.show()