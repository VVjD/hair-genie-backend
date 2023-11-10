import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.inception_v3 import preprocess_input
from django.conf import settings

def crop_face(image_path):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        raise ValueError("이미지에서 얼굴을 찾을 수 없습니다.")

    x, y, w, h = faces[0]
    x = max(0, x - 20)
    y = max(0, y - 20)
    cropped_image = image[y:y+h+40, x:x+w+40]

    return cropped_image

def predict_face_type(out_path):
    
    model = tf.keras.models.load_model('./models/fsmodel.h5')
    face_types = ['Heart', 'Oblong', 'Oval', 'Round', 'Square']

    img = image.load_img(out_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    preds = model.predict(x)
    top_pred_indices = np.argsort(preds[0])[::-1][:3]
    
    predictions = [{'type': face_types[i], 'probability': preds[0][i]} for i in top_pred_indices]

    return predictions