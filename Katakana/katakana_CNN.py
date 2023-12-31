import tensorflow as tf
from tensorflow import keras
import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from keras import backend as K

train_images = np.load("katakana_train_images.npz")['arr_0']
train_labels = np.load("katakana_train_labels.npz")['arr_0']
test_images = np.load("katakana_test_images.npz")['arr_0']
test_labels = np.load("katakana_test_labels.npz")['arr_0']

if K.image_data_format() == "channels_first": # reshape the image to be able to go through 2D CNN
  train_images = train_images.reshape(train_images.shape[0], 1,48,48)
  test_images2 = test_images.reshape(test_images.shape[0], 1,48,48)
  shape = (1,48,48)
else:
  train_images = train_images.reshape(train_images.shape[0], 48, 48, 1)
  test_images2 = test_images.reshape(test_images.shape[0], 48, 48, 1)
  shape = (48,48,1)

# the model
datagen = ImageDataGenerator(rotation_range=15,zoom_range=0.2)
datagen.fit(train_images)
model = keras.Sequential([
  keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=shape),
  keras.layers.MaxPooling2D(2,2),
  keras.layers.Conv2D(64, (3,3), activation='relu'),
  keras.layers.MaxPooling2D(2,2),
  keras.layers.Conv2D(64, (3,3), activation='relu'),
  keras.layers.MaxPooling2D(2,2),
  keras.layers.Flatten(),
  keras.layers.Dropout(0.5),
  keras.layers.Dense(512, activation='relu'),
  keras.layers.Dense(48, activation="softmax")
])

model.compile(optimizer='adam', loss="sparse_categorical_crossentropy", metrics=['accuracy'])

model.fit_generator(datagen.flow(train_images,train_labels,shuffle=True),epochs=30,validation_data=(test_images2,test_labels),callbacks = [keras.callbacks.EarlyStopping(patience=8,verbose=1,restore_best_weights=True),keras.callbacks.ReduceLROnPlateau(factor=0.5,patience=3,verbose=1)])

model.save("katakana-model.h5") 
