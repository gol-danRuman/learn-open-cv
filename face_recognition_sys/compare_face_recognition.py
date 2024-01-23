import os
import pickle

import cv2
import face_recognition
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

print("Loading Encode File ...")
file = open('EncodeFile.p', 'rb')
encode_list_known_with_names = pickle.load(file=file)
encode_list_known, name_list = encode_list_known_with_names
print("Encode File Loaded")

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    face_cur_frame = face_recognition.face_locations(imgS)
    encode_cur_frame = face_recognition.face_encodings(imgS, face_cur_frame)

    for encode_face, face_loc in zip(encode_cur_frame, face_cur_frame):
        matches = face_recognition.compare_faces(encode_list_known, encode_face)
        face_dis = face_recognition.face_distance(encode_list_known, encode_face)
        print("matches", matches)
        print("face_distace", face_dis)

        match_index = np.argmin(face_dis)

        if matches[match_index]:
            print("Known face detected")
            print(name_list[match_index])

    cv2.imshow("Face Attendance", img)
    cv2.waitKey(1)
