import cv2
import numpy as np
import face_recognition

imgElon = face_recognition.load_image_file('basic_images/Elon Musk.jpg')
imgElon = cv2.cvtColor(imgElon, cv2.COLOR_BGR2RGB)
imgTest = face_recognition.load_image_file('basic_images/Elon Test.jpeg')
imgTest = cv2.cvtColor(imgTest, cv2.COLOR_BGR2RGB)

facLoc = face_recognition.face_locations(imgElon)[0]
encodeElon = face_recognition.face_encodings(imgElon)[0]
cv2.rectangle(imgElon, (facLoc[3],facLoc[0]), (facLoc[1],facLoc[2]), (255,0,255), 2)

facLocTest = face_recognition.face_locations(imgTest)[0]
encodeTest = face_recognition.face_encodings(imgTest)[0]
cv2.rectangle(imgTest, (facLocTest[3],facLocTest[0]), (facLocTest[1],facLocTest[2]), (255,0,255), 2)

results = face_recognition.compare_faces([encodeElon], encodeTest)
print(results)

cv2.imshow('Elon Musk', imgElon)
cv2.imshow('Elon Test', imgTest)
cv2.waitKey(0)
