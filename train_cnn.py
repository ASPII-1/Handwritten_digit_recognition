import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import os


(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

#Normalize to [0,1]
x_train = x_train.astype("float32") / 255
x_test = x_test.astype("float32") / 255


x_train = x_train[..., tf.newaxis]
x_test = x_test[..., tf.newaxis]

model = keras.Sequential([
    layers.Conv2D(32, 3, activation='relu', input_shape=(28, 28, 1)),
    layers.MaxPooling2D(),
    layers.Conv2D(64, 3, activation='relu'),
    layers.MaxPooling2D(),
    layers.Flatten(),
    layers.Dense(10, activation='softmax')
])


model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])


model.fit(x_train, y_train, epochs=10, validation_data=(x_test, y_test))


if not os.path.exists('models'):
    os.makedirs('models')
model.save('models/cnn_mnist.h5')


test_loss, test_acc = model.evaluate(x_test, y_test)
print("Test accuracy:", test_acc)
