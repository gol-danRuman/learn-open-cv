from typing import Union
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, UploadFile, File, status
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import cv2
import face_recognition
import pickle
import numpy as np


print("Loading Encode File ...")
file = open('EncodeFile.p', 'rb')
encode_list_known_with_names = pickle.load(file=file)
encode_list_known, name_list = encode_list_known_with_names
print("Encode File Loaded")



app = FastAPI()


@app.post("/verify")
async def compare_face(file: Union[UploadFile, None] = None):
    if not file:
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder({"message": "No upload file sent"}),
        )
    else:
        # Read the image as a binary file
        try:
            status_code = 500
            image_binary = await file.read()
            if len(image_binary) < 1:
                return JSONResponse(
                        status_code=400,
                        content=jsonable_encoder({"error": "File Cannot be empty"}),
                    )

            # Convert the binary data to a NumPy array
            image_array = np.frombuffer(image_binary, np.uint8)

            # Decode the NumPy array as an image
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

            imgS = cv2.resize(image, (0, 0), None, 0.25, 0.25)
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
                    status_code = 200
                    print(name_list[match_index])
                    break
            if status_code == 200:
                return JSONResponse(
                    status_code=status_code,
                    content=jsonable_encoder({"status": "Face Detected", "user_name": name_list[match_index]}),
                )
            else:
                return JSONResponse(
                    status_code=status_code,
                    content=jsonable_encoder({'error': 'Something went wrong'}),
                )

        except Exception as error:
            print(str(error))

            return JSONResponse(
                status_code=status_code,
                content=jsonable_encoder({'error': str(error)}),
            )
