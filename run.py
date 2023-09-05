from keras.models import load_model
import cv2
import numpy as np


#cnn_mnist.h5
#lstm_mnist.h5
#hybrid_model.h5

model = load_model('models/hybrid_model.h5')


img = cv2.imread('user_image_hw.jpg', cv2.IMREAD_GRAYSCALE)

img = cv2.resize(img, (28, 28))
img = img.reshape(1, 28, 28)
img = img / 255

prediction = model.predict(img)
digit = np.argmax(prediction)

print(digit)
