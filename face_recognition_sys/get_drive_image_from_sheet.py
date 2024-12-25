from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
import gspread
import pickle
from oauth2client.service_account import ServiceAccountCredentials
import cv2
import io
import numpy as np
from typing import Dict, List, Any, Optional
import logging
from functools import lru_cache
from contextlib import contextmanager
import time
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import httplib2

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
SPREADSHEET_ID = "14SobbZCDKX9IKOJjY56G-WIOfVc7BctskqEKRG2ImAo"
FILE_ID = '1vAHnSq6eZWOy3YgbZ5LoSiQix6otb_XM'
FOLDER_ID = '1vdCwukuOiDZJOHRbyrOjRi7wksli8zkzkcViZopsyun4HrhO0ANo4bjemYDiXvEmh4oKd3jO'
SCOPES = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
CREDENTIALS_FILE = 'credentials.json'
RETRY_COUNT = 3
CHUNK_SIZE = 262144  # 256KB chunks for downloads

class GoogleAPIClient:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GoogleAPIClient, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPES)
        self._setup_http_retry()
        self.drive_service = None
        self.sheets_service = None
        self.gspread_client = None
        
    def _setup_http_retry(self):
        retry_strategy = Retry(
            total=RETRY_COUNT,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        self.http = httplib2.Http()
        self.http.timeout = 60  # 60 seconds timeout
        
    @property
    def drive(self):
        if not self.drive_service:
            self.drive_service = build('drive', 'v3', credentials=self.creds)
        return self.drive_service
    
    @property
    def sheets(self):
        if not self.sheets_service:
            self.sheets_service = build('sheets', 'v4', credentials=self.creds, http=self.http)
        return self.sheets_service
    
    @property
    def gspread(self):
        if not self.gspread_client:
            self.gspread_client = gspread.authorize(self.creds)
        return self.gspread_client

@lru_cache(maxsize=100)
def get_sheet_values(spreadsheet_id: str) -> List[Dict]:
    """Fetch and cache spreadsheet values."""
    client = GoogleAPIClient()
    try:
        sheet = client.gspread.open_by_key(spreadsheet_id)
        sheet_instance = sheet.get_worksheet(0)
        records_data = sheet_instance.get_all_records()
        logger.info(f"Successfully fetched {len(records_data)} records from sheets")
        return records_data
    except HttpError as error:
        logger.error(f"Failed to read sheets: {error}")
        raise

@lru_cache(maxsize=1000)
def get_image(image_id: str) -> Optional[np.ndarray]:
    """Fetch and cache image from Google Drive."""
    client = GoogleAPIClient()
    try:
        request = client.drive.files().get_media(fileId=image_id)
        file_buffer = io.BytesIO()
        downloader = MediaIoBaseDownload(file_buffer, request, chunksize=CHUNK_SIZE)
        
        done = False
        while not done:
            _, done = downloader.next_chunk()
            
        jpg_as_np = np.frombuffer(file_buffer.getvalue(), dtype=np.uint8)
        img = cv2.imdecode(jpg_as_np, flags=1)
        return img
        
    except HttpError as error:
        logger.error(f"Failed to fetch image {image_id}: {error}")
        return None

@contextmanager
def pickle_file_handler(filename: str, mode: str):
    """Context manager for handling pickle files."""
    file = None
    try:
        file = open(filename, mode)
        yield file
    finally:
        if file:
            file.close()

def update_to_drive(encode_list_known: List[Any]) -> None:
    """Update existing file in Google Drive."""
    client = GoogleAPIClient()
    try:
        logger.info("Saving encoded model...")
        with pickle_file_handler("EncodeFile.p", "wb") as file:
            pickle.dump(encode_list_known, file)
        
        file_metadata = {'name': 'EncodeFile.p'}
        media = MediaFileUpload('EncodeFile.p', 
                              mimetype='application/octet-stream',
                              resumable=True)
        
        file = client.drive.files().update(
            fileId=FILE_ID,
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        
        logger.info(f"File updated successfully. ID: {file.get('id')}")
        
    except HttpError as error:
        logger.error(f"Failed to update file: {error}")
        raise

def create_to_drive_in_folder(encode_list_known: List[Any]) -> None:
    """Create new file in Google Drive folder."""
    client = GoogleAPIClient()
    try:
        logger.info("Saving encoded model...")
        with pickle_file_handler("EncodeFile.p", "wb") as file:
            pickle.dump(encode_list_known, file)
        
        file_metadata = {
            'name': 'EncodeFile.p',
            'parents': [FOLDER_ID]
        }
        media = MediaFileUpload('EncodeFile.p',
                              mimetype='application/octet-stream',
                              resumable=True)
        
        file = client.drive.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        
        logger.info(f"File created successfully. ID: {file.get('id')}")
        
    except HttpError as error:
        logger.error(f"Failed to create file: {error}")
        raise

def load_model_file() -> Optional[io.BytesIO]:
    """Load model file from Google Drive."""
    client = GoogleAPIClient()
    try:
        request = client.drive.files().get_media(fileId=FILE_ID)
        file_buffer = io.BytesIO()
        downloader = MediaIoBaseDownload(file_buffer, request, chunksize=CHUNK_SIZE)
        
        done = False
        while not done:
            status, done = downloader.next_chunk()
            logger.info(f"Download progress: {int(status.progress() * 100)}%")
            
        return file_buffer
        
    except HttpError as error:
        logger.error(f"Failed to load model file: {error}")
        return None

if __name__ == "__main__":
    try:
        rows = get_sheet_values(SPREADSHEET_ID)
        for row in rows:
            image_id = row['Share Passport Photo (>1MB)'].split("id=")[1]
            get_image(image_id)
    except Exception as e:
        logger.error(f"Main execution failed: {e}")



