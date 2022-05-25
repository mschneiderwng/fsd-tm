#!/usr/bin/env python
import cv2  # import opencv
import keras as keras
import numpy as np

np.set_printoptions(suppress=True)

webcam = cv2.VideoCapture(0)
model = keras.models.load_model('src/keras_model.h5')
data_for_model = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)


def load_labels(path):
    f = open(path, 'r')
    lines = f.readlines()
    labels = []
    for line in lines:
        labels.append(line.split(' ')[1].strip('\n'))
    return labels


label_path = 'src/labels.txt'
labels = load_labels(label_path)
print(labels)

# This function proportionally resizes the image from your webcam to 224 pixels high


def image_resize(image, height, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]
    r = height / float(h)
    dim = (int(w * r), height)
    resized = cv2.resize(image, dim, interpolation=inter)
    return resized

# this function crops to the center of the resize image


def cropTo(img):
    size = 224
    height, width = img.shape[:2]

    sideCrop = (width - 224) // 2
    return img[:, sideCrop:(width - sideCrop)]


while True:
    ret, img = webcam.read()
    if ret:
        # same as the cropping process in TM2
        img = image_resize(img, height=224)
        img = cropTo(img)

        # flips the image
        img = cv2.flip(img, 1)

        # normalize the image and load it into an array that is the right format for keras
        normalized_img = (img.astype(np.float32) / 127.0) - 1
        data_for_model[0] = normalized_img

        # run inference
        prediction = model.predict(data_for_model)
        for i in range(0, len(prediction[0])):
            print('{}: {}'.format(labels[i], prediction[0][i]))
        cv2.imshow('webcam', img)
        if cv2.waitKey(1) == 27:
            break

cv2.destroyAllWindows()
