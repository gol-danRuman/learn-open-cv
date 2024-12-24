from typing import Union
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import JSONResponse
import cv2
import face_recognition
import pickle
import numpy as np
from get_drive_image_from_sheet import load_model_file
from encode_generator import main as encoding

print("Loading Encode File ...")
# file = open('EncodeFile.p', 'rb')
# encode_list_known_with_names = pickle.load(file=file)
# encode_list_known, name_list = encode_list_known_with_names
file_buffer = load_model_file()
file_buffer.seek(0)
encode_list_known_with_names = pickle.load(file=file_buffer)
encode_list_known, name_list = encode_list_known_with_names
print("Encode File Loaded")

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://face-recognition-sys-frontend.onrender.com",
    "https://face-recognition-sys-frontend.onrender.com/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def initial_load():
    return JSONResponse(
        status_code=200,
        content=jsonable_encoder({"message": "Api working"}),
    )


@app.post("/verify")
async def compare_face(
    file: UploadFile = File(...)
):
    try:
        status_code = 500
        image_binary = await file.read()
        if len(image_binary) < 1:
            return JSONResponse(
                status_code=400,
                content=jsonable_encoder({"message": "File Cannot be empty"}),
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
                content=jsonable_encoder({'message': 'Something went wrong'}),
            )

    except Exception as error:
        print(str(error))

        return JSONResponse(
            status_code=status_code,
            content=jsonable_encoder({'error': str(error)}),
        )


@app.get("/start-encoding")
async def encode_model():
    try:
        encoding()

        return JSONResponse(
            status_code=200,
            content=jsonable_encoder({"status": "Success", "message": "Encoded and uploaded to model to drive"}),
        )
    except Exception as error:
        print(str(error))

        return JSONResponse(
            status_code=500,
            content=jsonable_encoder({'error': str(error)}),
        )
