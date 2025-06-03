import tensorflow as tf
import matplotlib.pyplot as plt

mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()

# print(len(x_train))
# print("---")
# print(len(x_test))
# print("------")

# print(x_train[0])
# print("---")
# print(x_test[0])

# plt.imshow(x_train[2], cmap = 'gray')
# plt.show()

#normalization
x_train = x_train/ 255.0
x_test = x_test / 255.0

#convlutional layer
x_train = x_train[..., tf.newaxis]
x_test = x_test[..., tf.newaxis]

train_data = tf.data.Dataset.from_tensor_slices((x_train, y_train)).shuffle(10000).batch(32)
test_data = tf.data.Dataset.from_tensor_slices((x_test, y_test)).batch(32)

print(train_data)

print('end')