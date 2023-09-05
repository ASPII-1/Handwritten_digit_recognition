import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.datasets import mnist
import numpy as np
import gzip
import os

data_dir='./MNIST_data'

def load_mnist():
    with gzip.open(os.path.join(data_dir, 'train-images-idx3-ubyte.gz'), 'rb') as f:
        x_train = np.frombuffer(f.read(), np.uint8, offset=16).reshape(-1, 28, 28, 1)
    with gzip.open(os.path.join(data_dir, 'train-labels-idx1-ubyte.gz'), 'rb') as f:
        y_train = np.frombuffer(f.read(), np.uint8, offset=8)
    with gzip.open(os.path.join(data_dir, 't10k-images-idx3-ubyte.gz'), 'rb') as f:
        x_test = np.frombuffer(f.read(), np.uint8, offset=16).reshape(-1, 28, 28, 1)
    with gzip.open(os.path.join(data_dir, 't10k-labels-idx1-ubyte.gz'), 'rb') as f:
        y_test = np.frombuffer(f.read(), np.uint8, offset=8)
    return (x_train, y_train), (x_test, y_test)

# mnist.load_data()
(x_train, y_train), (x_test, y_test) = mnist.load_data()

#Normalize
x_train = x_train.astype('float32') / 255
x_test = x_test.astype('float32') / 255


x_train = np.expand_dims(x_train, axis=-1)
x_test = np.expand_dims(x_test, axis=-1)


#CNN
cnn_model = tf.keras.Sequential([
    layers.Conv2D(32, (3,3), activation='relu', input_shape=(28,28,1)),
    layers.MaxPooling2D((2,2)),
    layers.Conv2D(64, (3,3), activation='relu'),
    layers.MaxPooling2D((2,2)),
    layers.Flatten()
])

#LSTM
lstm_model = tf.keras.Sequential([
    layers.LSTM(128),
    layers.Dense(10, activation='softmax')
])

#Hybrid
hybrid_model = tf.keras.Sequential([
    cnn_model,
    layers.Reshape((-1, 1600)),
    lstm_model
])


hybrid_model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])


hybrid_model.fit(x_train, y_train, epochs=5, validation_data=(x_test, y_test))


if not os.path.exists('models'):
    os.makedirs('models')
hybrid_model.save('models/hybrid_model.h5')

#Load from saved
loaded_model = tf.keras.models.load_model('hybrid_model.h5')

predictions = loaded_model.predict(x_test[:10])
print(np.argmax(predictions, axis=1))
