import os
import pickle
import cv2
import face_recognition
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

print("Loading Encode File ...")
with open('EncodeFile.p', 'rb') as file:
    encode_list_known, name_list = pickle.load(file)
print("Encode File Loaded")

while True:
    success, img = cap.read()
    if not success:
        continue

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25, interpolation=cv2.INTER_AREA)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    
    face_cur_frame = face_recognition.face_locations(imgS, model='hog')
    if face_cur_frame:
        encode_cur_frame = face_recognition.face_encodings(imgS, face_cur_frame)

        for encode_face, face_loc in zip(encode_cur_frame, face_cur_frame):
            matches = face_recognition.compare_faces(encode_list_known, encode_face, tolerance=0.6)
            face_dis = face_recognition.face_distance(encode_list_known, encode_face)
            
            if any(matches):
                match_index = np.argmin(face_dis)
                if matches[match_index]:
                    name = name_list[match_index]
                    print(f"Known face detected: {name}")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
