import numpy as np
import tensorflow as tf
from tensorflow import keras
from matplotlib import pyplot as plt

fashion_images = keras.datasets.fashion_mnist
(train_images, train_labels), (test_images, test_labels) = fashion_images.load_data()

# print(train_images.shape)

# print(*train_images[0])

index = 8754
plt.imshow(train_images[index], cmap = plt.cm.binary)
plt.show()

model = keras.Sequential([
    keras.layers.Flatten(input_shape = (28, 28)),
    keras.layers.Dense(128, activation = tf.nn.relu), #rectified linear unit
    keras.layers.Dense(64, activation = tf.nn.relu),
    keras.layers.Dense(32, activation = tf.nn.relu),
    keras.layers.Dense(10, activation = tf.nn.softmax) #picks the largest probability of the item picked
])

model.compile(
    optimizer = 'adam',
    loss = 'sparse_categorical_crossentropy',
    metrics = ['accuracy']
)

model.fit(train_images, train_labels, epochs = 5)
model.evaluate(test_images, test_labels)

# used to predict new images
predictions = model.predict()