# -*- coding: utf-8 -*-
"""VGG16.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KotNQ3E4EAuthbknA_ZE9yu6Zf7wCwkC
"""

from keras.layers import Input, Lambda, Dense, Flatten
from keras.models import Model
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
import numpy as np
from glob import glob
import matplotlib.pyplot as plt

from google.colab import drive
drive.mount("/content/gdrive")

from zipfile import ZipFile
file_name="/content/gdrive/My Drive/Project Dataset/tomato.zip"

with ZipFile(file_name,'r') as zip:
  zip.extractall()
  print('Done')

IMAGE_SIZE = [224, 224]

train_path = '/content/tomato/train/'
valid_path = '/content/tomato/val/'

vgg = VGG16(input_shape=IMAGE_SIZE + [3], weights='imagenet', include_top=False)

# don't train existing weights
for layer in vgg.layers:
  layer.trainable = False

# useful for getting number of classes
folders = glob('/content/tomato/train/*')

# our layers - you can add more if you want
x = Flatten()(vgg.output)
# x = Dense(1000, activation='relu')(x)
prediction = Dense(len(folders), activation='softmax')(x)

# create a model object
model = Model(inputs=vgg.input, outputs=prediction)

# view the structure of the model
model.summary()

# tell the model what cost and optimization method to use
model.compile(
  loss='categorical_crossentropy',
  optimizer='adam',
  metrics=['accuracy']
)

from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1./255)

training_set = train_datagen.flow_from_directory('/content/tomato/train/',
                                                 target_size = (224, 224),
                                                 batch_size = 32,
                                                 class_mode = 'categorical')

test_set = test_datagen.flow_from_directory('/content/tomato/val',
                                            target_size = (224, 224),
                                            batch_size = 32,
                                            class_mode = 'categorical')

'''r=model.fit_generator(training_set,
                         samples_per_epoch = 8000,
                         nb_epoch = 5,
                         validation_data = test_set,
                         nb_val_samples = 2000)'''

r = model.fit_generator(
  training_set,
  validation_data=test_set,
  epochs=5,
  steps_per_epoch=len(training_set),
  validation_steps=len(test_set)
)

import tensorflow as tf

from keras.models import load_model

model.save('Dataset_new_model.h5')

from google.colab import drive
drive.mount('/content/gdrive')

model.save('/content/gdrive/My Drive/model.h5')

import cv2
import tensorflow as tf
def prepare(filepath):
    img_array = cv2.imread(filepath, cv2.IMREAD_COLOR)
    img_array = img_array / 255
    new_array = cv2.resize(img_array, (224, 224))
    return new_array.reshape(-1, 224, 224, 3)

model = tf.keras.models.load_model("/content/Dataset_new_model.h5")

prediction = model.predict([prepare("/content/tomato/val/Tomato___Bacterial_spot/01f13167-f508-4ef2-8720-4e973438f8fc___GCREC_Bact.Sp 5892.JPG")])
np.argmax(prediction)

class_dict = training_set.class_indices
class_dict

prediction = model.predict([prepare("/content/tomato/val/Tomato___Bacterial_spot/0d922399-7ba5-4d12-b84e-bb4b966c58ae___GCREC_Bact.Sp 6307.JPG")])

if np.argmax(prediction) == 0:
    print("Bacterial_spot")
elif np.argmax(prediction) == 1:
    print("Early_Blight")
elif np.argmax(prediction) == 2:
    print("Late Blight")
elif np.argmax(prediction) == 3:
    print("Leaf Mold")
elif np.argmax(prediction) == 4:
    print("Septoria Leaf Mold")
elif np.argmax(prediction) == 5:
    print("Spider mites")
elif np.argmax(prediction) == 6:
    print("Target Spot")
elif np.argmax(prediction) == 7:
    print("Yellow Leaf Curl Virus")
elif np.argmax(prediction) == 8:
    print("Mosaic Virus")
else:
    print("Healthy")

model.save_weights("/content/gdrive/My Drive/train.pickle")