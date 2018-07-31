
import numpy as np
import os
import cv2
import dlib


def cosine_distance(vec1, vec2):
  """

    Calculate the similarity of two vectors
  """
  npvec1, npvec2 = np.asarray(vec1), np.asarray(vec2)
  num = np.dot(npvec1.T, npvec2)
  denom = np.linalg.norm(npvec1) * np.linalg.norm(npvec2)
  cos = num / denom

  return cos


def get_face(imgpath):
    """
    Get face region from image, use opencv haar features
    """
    #Create the haar cascade
    modelxml = "./config/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(modelxml)

    #Read the image
    image = cv2.imread(imgpath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #Detect faces in the image
    faces = faceCascade.detectMultiScale(gray,
                                         scaleFactor=1.1,
                                         minNeighbors=5,
                                         minSize=(30, 30))

    for(x, y, w, h) in faces:
        img_crop = image[y:y+h, x:x+w]

    return img_crop


def get_face_dlib(imgpath):
    """
    Get face region from image, use dlib
    """
    print imgpath
    detector = dlib.get_frontal_face_detector()

    img = cv2.imread(imgpath)
<<<<<<< Updated upstream

    if img.shape[0] * img.shape[1] > 500000:
        img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
    dets = detector(img, 1)
=======
    if img:
        if img.shape[0] * img.shape[1] > 500000:
            img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
        dets = detector(img, 1)
>>>>>>> Stashed changes

    images = []
    for k, d in enumerate(dets):
        rec = dlib.rectangle(d.left(), d.top(), d.right(), d.bottom())
        crop_image = img[d.top():d.bottom(), d.left():d.right()]
        # cv2.rectangle(img, (rec.left(), rec.top()), (rec.right(), rec.bottom()), (0, 255, 0), 2)
        images.append(crop_image)

        # cv2.imshow('image', img)
        # cv2.waitKey(0)

    return images[0]


def listdir(path):
    list_name = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            listdir(file_path)
        else:
            list_name.append(file_path)
    list_name.sort()
    return list_name




