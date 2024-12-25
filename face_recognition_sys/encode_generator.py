import cv2
import face_recognition
import pickle
from typing import List, Tuple, Dict, Any
from tqdm import tqdm
import logging
from contextlib import contextmanager
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial

from get_drive_image_from_sheet import get_image, get_sheet_values, update_to_drive

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
SPREADSHEET_ID = "14SobbZCDKX9IKOJjY56G-WIOfVc7BctskqEKRG2ImAo"
BATCH_SIZE = 10
MAX_WORKERS = 4  # Adjust based on your CPU cores
FACE_DETECTION_MODEL = 'hog'  # Use 'cnn' for GPU support

def process_single_image(img: np.ndarray, index: int) -> Tuple[np.ndarray, bool]:
    try:
        # Resize image for faster face detection
        scale_factor = 0.5
        small_frame = cv2.resize(img, (0, 0), fx=scale_factor, fy=scale_factor)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        # Detect face locations on smaller image
        face_locations = face_recognition.face_locations(
            rgb_small_frame, 
            model=FACE_DETECTION_MODEL
        )
        
        if not face_locations:
            logger.warning(f"No face detected in image at index: {index}")
            return None, False
            
        # Adjust face locations back to original size
        face_locations_original = [(
            int(top/scale_factor),
            int(right/scale_factor),
            int(bottom/scale_factor),
            int(left/scale_factor)
        ) for top, right, bottom, left in face_locations]
        
        # Convert to RGB for face_recognition
        rgb_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_encodings = face_recognition.face_encodings(
            rgb_frame, 
            face_locations_original
        )
        
        return face_encodings[0] if face_encodings else None, True
        
    except Exception as e:
        logger.error(f"Error processing image at index {index}: {str(e)}")
        return None, False

def find_encodings(images_list: List[np.ndarray]) -> List[np.ndarray]:
    encode_list = []
    
    # Create a partial function with just the index parameter remaining
    process_func = partial(process_single_image)
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Submit all tasks and map them to their indices
        future_to_index = {
            executor.submit(process_func, img, idx): idx 
            for idx, img in enumerate(images_list)
        }
        
        # Process results as they complete
        for future in tqdm(
            as_completed(future_to_index), 
            total=len(images_list),
            desc="Processing faces"
        ):
            idx = future_to_index[future]
            try:
                encoding, success = future.result()
                if success and encoding is not None:
                    encode_list.append(encoding)
            except Exception as e:
                logger.error(f"Error processing future at index {idx}: {str(e)}")
    
    return encode_list

@contextmanager
def save_pickle(filename: str):
    try:
        with open(filename, "wb") as file:
            yield file
    finally:
        pass  # File is automatically closed by context manager

def save_model(encode_list_known: List[Any]) -> None:
    logger.info("Saving encoded model...")
    try:
        with save_pickle("EncodeFile.p") as file:
            pickle.dump(encode_list_known, file)
        logger.info("Model saved successfully")
    except Exception as e:
        logger.error(f"Error saving model: {str(e)}")

def process_sheet_data(rows: List[Dict]) -> Tuple[List, List[str]]:
    images_list = []
    name_list = []
    
    # Process in batches for better memory management
    batch = []
    for idx, row in enumerate(tqdm(rows, desc="Fetching images")):
        try:
            image_id = row['Share Passport Photo (>1MB)'].split("id=")[1]
            batch.append((image_id, row['Name']))
            
            if len(batch) >= BATCH_SIZE or idx == len(rows) - 1:
                # Process batch
                with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                    future_to_id = {
                        executor.submit(get_image, img_id): (img_id, name)
                        for img_id, name in batch
                    }
                    
                    for future in as_completed(future_to_id):
                        img_id, name = future_to_id[future]
                        try:
                            img = future.result()
                            if img is not None:
                                images_list.append(img)
                                name_list.append(name)
                        except Exception as e:
                            logger.error(f"Error fetching image {img_id}: {str(e)}")
                
                batch = []  # Clear batch
                
        except Exception as e:
            logger.error(f"Error processing row {row.get('Name', 'Unknown')}: {str(e)}")
            
    return images_list, name_list

def main() -> None:
    path = 'Images'
    images = []
    user_data = []
    
    # Get user details from spreadsheet
    sheet_data = get_sheet_values(SPREADSHEET_ID)

    # Try to load existing encodings
    try:
        with open("EncodeFile.p", "rb") as file:
            existing_encode_list, existing_user_data = pickle.load(file)
        logger.info(f"Loaded {len(existing_encode_list)} existing encodings")
    except (FileNotFoundError, EOFError):
        existing_encode_list = []
        existing_user_data = []
        logger.info("No existing encodings found")

    # Track new entries
    new_encodings = []
    new_user_data = []
    
    for row in sheet_data:
        try:
            # Make sure the image ID exists in the row
            if 'Share Passport Photo (>1MB)' not in row:
                logger.warning(f"Missing photo URL for user: {row.get('Full Name', 'Unknown')}")
                continue

            # Create user info dictionary
            user_info = {
                'name': row.get('Name', 'N/A'),
                'email': row.get('Email', 'N/A'),
                'contact': row.get('Phone number', 'N/A')
            }

            # Check if user already exists
            if user_info not in existing_user_data:
                image_id = row['Share Passport Photo (>1MB)'].split("id=")[1]
                img = get_image(image_id)
                if img is not None:
                    images.append(img)
                    user_data.append(user_info)
                    logger.info(f"Added new user: {user_info['name']}")
            else:
                logger.info(f"User {user_info['name']} already exists, skipping")

        except Exception as e:
            logger.error(f"Error processing row: {e}")
            continue
    
    # Only encode if there are new images
    if images:
        logger.info(f"Processing {len(images)} new images for encoding...")
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            new_encodings.append(encode)
        
        # Combine existing and new data
        final_encode_list = existing_encode_list + new_encodings
        final_user_data = existing_user_data + user_data
        
        encode_list_with_data = [final_encode_list, final_user_data]
        logger.info(f"Total encodings after update: {len(final_encode_list)}")
        
        # Save the updated encodings
        logger.info("Saving updated model...")
        with open("EncodeFile.p", "wb") as file:
            pickle.dump(encode_list_with_data, file)
        
        # Upload to drive
        logger.info("Uploading updated model to drive...")
        update_to_drive(encode_list_with_data)
        logger.info("Upload completed successfully")
    else:
        logger.info("No new users to encode")

if __name__ == '__main__':
    main()
