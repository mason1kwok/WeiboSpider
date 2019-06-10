import sys
import dlib
import urllib.request
import numpy
import cv2
import face_recognition
import os

face_detector = dlib.get_frontal_face_detector()

def url2img(url):
    resp = urllib.request.urlopen(url)
    try:
        img = numpy.asarray(bytearray(resp.read()), dtype='uint8')
    except:
        return None
    return cv2.imdecode(img, cv2.IMREAD_COLOR)


def url2faces(url):
    img = url2img(url)
    if img is None or len(img) <= 0:
        return []
    detected_faces = face_detector(img, 1)
    faces = []
    for i, face_rect in enumerate(detected_faces):
        # Detected faces are returned as an object with the coordinates
        # of the top, left, right and bottom edges
    
        crop = img[face_rect.top():face_rect.bottom(), face_rect.left():face_rect.right()]
        encodings = face_recognition.face_encodings(crop)
        faces.append(encodings)
    return faces

    

