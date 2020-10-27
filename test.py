import streamlit as st
import tensorflow as tf

st.set_option('deprecation.showfileUploaderEncoding',False)
@st.cache(allow_output_mutation=True)
def load_model():
  model = tf.keras.models.load_model("/content/gdrive/My Drive/Project Dataset/model1.h5")
  return model
model=load_model()
st.write("""
         # Tomato Leaf Disease Classification
         """  )
file= st.file_uploader("Upload the leaf image",type=["jpg","png"])
import cv2
from PIL import Image, ImageOps
import numpy as np
def prepare(file):
    img_array = cv2.imread(filepath, cv2.IMREAD_COLOR)
    img_array = img_array / 255
    new_array = cv2.resize(img_array, (224, 224))
    return new_array.reshape(-1, 224, 224, 3)

  

if file is None:
  st.text("Upload an image")
else:
  image=Image.open(file)
  st.image(image,use_column_width=True)
  predictions=model.predict([prepare(image)])
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

