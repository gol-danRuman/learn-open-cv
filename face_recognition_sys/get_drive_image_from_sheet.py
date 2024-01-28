
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
import gspread
import pickle
from oauth2client.service_account import ServiceAccountCredentials

SPREADSHEET_ID = "14SobbZCDKX9IKOJjY56G-WIOfVc7BctskqEKRG2ImAo"
# Link to Drive: https://drive.google.com/drive/u/0/folders/1vdCwukuOiDZJOHRbyrOjRi7wksli8zkzkcViZopsyun4HrhO0ANo4bjemYDiXvEmh4oKd3jO
FILE_ID = '1vAHnSq6eZWOy3YgbZ5LoSiQix6otb_XM'
FOLDER_ID = '1vdCwukuOiDZJOHRbyrOjRi7wksli8zkzkcViZopsyun4HrhO0ANo4bjemYDiXvEmh4oKd3jO'
def get_sheet_values(spreadsheet_id):
    """
    Creates the batch_update the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    # pylint: disable=maybe-no-member
    try:
        service = build("sheets", "v4", credentials=creds)

        client = gspread.authorize(creds)
        sheet = client.open_by_key(spreadsheet_id)
        sheet_instance = sheet.get_worksheet(0)
        records_data = sheet_instance.get_all_records()
        print(f"Records in Sheets : {records_data}")
        return records_data
    except HttpError as error:
        print(f"An error occurred while reading sheets: {error}")
        return error


def get_image(image_id):
    import cv2
    import io
    import numpy as np
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    try:
        service = build('drive', 'v3', credentials=creds)
        request = service.files().get_media(fileId=image_id)
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        jpg_as_np = np.frombuffer(file.getvalue(), dtype=np.uint8)
        img = cv2.imdecode(jpg_as_np, flags=1)
        return img
        # cv2.imshow('Photo', img)
        # cv2.waitKey(0)

    except HttpError as error:
        print(f"An error occurred while getting image: {error}")
        return error

def update_to_drive(encode_list_known):

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    try:
        service = build('drive', 'v3', credentials=creds)

        print("Saving Encoded model....")
        file = open("EncodeFile.p", "wb")
        pickle.dump(encode_list_known, file)
        file.close()
        file_metadata = {'name': 'EncodeFile.p'}
        media = MediaFileUpload('EncodeFile.p', mimetype='application/octet-stream')
        file = service.files().update(fileId=FILE_ID,body=file_metadata, media_body=media,fields='id').execute()
        print(f"File: {file}")
        print(f'File ID: {file.get("id")}')

    except HttpError as error:
        print(f"An error occurred while getting image: {error}")
        return error


def create_to_drive_in_folder(encode_list_known):

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    try:
        service = build('drive', 'v3', credentials=creds)

        print("Saving Encoded model....")
        file = open("EncodeFile.p", "wb")
        pickle.dump(encode_list_known, file)
        file.close()
        file_metadata = {'name': 'EncodeFile.p', 'parents': [FOLDER_ID]}
        media = MediaFileUpload('EncodeFile.p', mimetype='application/octet-stream')
        file = service.files().create(fileId=FILE_ID,body=file_metadata, media_body=media,fields='id').execute()
        print(f"File: {file}")
        print(f'File ID: {file.get("id")}')

    except HttpError as error:
        print(f"An error occurred while getting image: {error}")
        return error


def load_model_file():
    import io
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    try:
        service = build('drive', 'v3', credentials=creds)
        file_id = FILE_ID

        # pylint: disable=maybe-no-member
        request = service.files().get_media(fileId=file_id)
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}.")

        # print(file, file.getvalue())
        return file

    except HttpError as error:
        print(f"An error occurred while getting image: {error}")
        return error

if __name__ == "__main__":

    # Pass: spreadsheet_id, and range_name
    rows = get_sheet_values(SPREADSHEET_ID)

    for row in rows:
        # print(row['Share Passport Photo (>1MB)'].split("id=")[1])
        get_image(row['Share Passport Photo (>1MB)'].split("id=")[1])



