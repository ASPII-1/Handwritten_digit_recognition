import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import os


(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

#Normalize image pixels to [0,1]
x_train = x_train.astype("float32") / 255
x_test = x_test.astype("float32") / 255

#Make rows from images
x_train = x_train.reshape((x_train.shape[0], 28, 28))
x_test = x_test.reshape((x_test.shape[0], 28, 28))

model = keras.Sequential([
    layers.LSTM(128, input_shape=(28, 28)),
    layers.Dense(10, activation='softmax')
])


model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])


model.fit(x_train, y_train, epochs=5, validation_data=(x_test, y_test))


if not os.path.exists('models'):
    os.makedirs('models')
model.save('models/lstm_mnist.h5')

#Check Accuracy
test_loss, test_acc = model.evaluate(x_test, y_test)
print("Test accuracy:", test_acc)