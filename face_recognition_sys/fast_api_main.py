from typing import Union, Dict, List
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
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

print("Loading Encode File and User Data...")
file_buffer = load_model_file()
if file_buffer is None:
    logger.error("Failed to load model file")
    raise RuntimeError("Failed to load face recognition model file")

file_buffer.seek(0)
encode_list_known_with_data = pickle.load(file=file_buffer)
encode_list_known, user_list = encode_list_known_with_data
logger.info(f"Encode File Loaded with {len(user_list)} faces")

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
        logger.info("Starting face verification process")
        
        image_binary = await file.read()
        if len(image_binary) < 1:
            logger.warning("Received empty file")
            return JSONResponse(
                status_code=400,
                content=jsonable_encoder({"message": "File Cannot be empty"}),
            )

        logger.info(f"Received image of size: {len(image_binary)} bytes")

        # Convert the binary data to a NumPy array
        image_array = np.frombuffer(image_binary, np.uint8)
        logger.info("Converted image to numpy array")

        # Decode the NumPy array as an image
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        if image is None:
            logger.error("Failed to decode image")
            return JSONResponse(
                status_code=400,
                content=jsonable_encoder({"message": "Invalid image format"}),
            )

        logger.info("Successfully decoded image")

        imgS = cv2.resize(image, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        face_cur_frame = face_recognition.face_locations(imgS)
        logger.info(f"Found {len(face_cur_frame)} faces in image")
        
        if not face_cur_frame:
            logger.warning("No faces detected in the image")
            return JSONResponse(
                status_code=400,
                content=jsonable_encoder({
                    "message": "Please upload a photo with a clear image where face, eyes, and ears are properly visible"
                }),
            )

        encode_cur_frame = face_recognition.face_encodings(imgS, face_cur_frame)
        logger.info("Generated face encodings")

        for encode_face, face_loc in zip(encode_cur_frame, face_cur_frame):
            matches = face_recognition.compare_faces(encode_list_known, encode_face)
            face_dis = face_recognition.face_distance(encode_list_known, encode_face)
            logger.info(f"Face matches: {matches}")
            logger.info(f"Face distances: {face_dis}")

            match_index = np.argmin(face_dis)

            if matches[match_index]:
                # Get user details from the matched index
                user_details = user_list[match_index]
                
                # Handle both string and dictionary user details
                if isinstance(user_details, dict):
                    name = user_details.get('name', 'Unknown')
                    email = user_details.get('email', 'N/A')
                    contact = user_details.get('contact', 'N/A')
                else:
                    # If user_details is a string, use it as the name
                    name = str(user_details)
                    email = 'N/A'
                    contact = 'N/A'
                
                logger.info(f"Known face detected: {name}")
                status_code = 200
                
                return JSONResponse(
                    status_code=status_code,
                    content=jsonable_encoder({
                        "status": "Face Detected",
                        "user_data": {
                            "name": name,
                            "email": email,
                            "contact": contact
                        }
                    }),
                )
        
        logger.warning("No matching face found")
        return JSONResponse(
            status_code=401,
            content=jsonable_encoder({
                'message': 'Face not recognized. Please ensure you have signed up or try uploading a clearer photo.'
            }),
        )

    except Exception as error:
        logger.error(f"Error in face verification: {str(error)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder({
                'error': 'Please upload a photo with a clear image where face, eyes, and ears are properly visible'
            }),
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
