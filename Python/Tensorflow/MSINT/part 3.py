import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.layers import Conv2D, Flatten, Dense
import matplotlib.pyplot as plt

mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()

#normalization
x_train = x_train / 255.0
x_test = x_test / 255.0

#convlutional layer
x_train = x_train[..., tf.newaxis]
x_test = x_test[..., tf.newaxis]

train_data = tf.data.Dataset.from_tensor_slices((x_train, y_train)).shuffle(10000).batch(32)
test_data = tf.data.Dataset.from_tensor_slices((x_test, y_test)).batch(32)

class MNISTModel(Model):
    def __init__(self):
        super(MNISTModel, self).__init__()
        self.conv1 = Conv2D(32, 3, activation = 'relu') #outputs input or 0 at min
        self.flatten = Flatten()
        self.dense1 = Dense(128, activation = 'relu')
        self.dense2 = Dense(10, activation = 'softmax') #calculating dist or prob dist

    def __call__(self, x):
        x1 = self.conv1(x)
        x2 = self.flatten(x1)
        x3 = self.dense1(x2)
        return self.dense2(x3)

model = MNISTModel()

loss_function = tf.keras.losses.SparseCategoricalCrossentropy()
optimizer = tf.keras.optimizers.Adam()

train_loss = tf.keras.metrics.Mean(name = "train_loss")
train_acc = tf.keras.metrics.SparseCategoricalAccuracy(name = "train_acc")

test_loss = tf.keras.metrics.Mean(name = "test_loss")
test_acc = tf.keras.metrics.SparseCategoricalAccuracy(name = "test_acc")

@tf.function
def train_step(inputs, labels):
    with tf.GradientTape() as gt:
        predictions = model(inputs)
        loss = loss_function(labels, predictions)

    gradients = gt.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))

    train_loss(loss)
    train_acc(labels, predictions)

@tf.function
def test_step(inputs, labels):
    predictions = model(inputs)
    loss = loss_function(labels, predictions)

    test_loss(loss)
    test_acc(labels, predictions)

epochs = 5

for epoch in range(epochs):

    for train_inputs, train_labels in train_data:
        train_step(train_inputs, train_labels)

    for test_inputs, test_labels in test_data:
        test_step(test_inputs, test_labels)

    template = "Epoch {}, Train loss: {}, Train acc: {}, Test loss: {}, Test acc: {}"
    print(template.format(
        epoch + 1,
        train_loss.result(),
        train_acc.result(),
        test_loss.result(),
        test_acc.result()
    ))

    train_loss.reset_state()
    train_acc.reset_state()
    test_loss.reset_state()
    test_acc.reset_state()

print('end')