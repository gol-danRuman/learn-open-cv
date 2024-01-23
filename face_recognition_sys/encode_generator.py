import cv2
import face_recognition
import pickle

from get_drive_image_from_sheet import get_image, get_sheet_values

SPREADSHEET_ID = "14SobbZCDKX9IKOJjY56G-WIOfVc7BctskqEKRG2ImAo"


def find_encodings(images_list):
    encode_list = []
    for img in images_list:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encode_list.append(encode)
    print(encode_list)
    return encode_list


if __name__ == '__main__':
    rows = get_sheet_values(SPREADSHEET_ID)
    images_list = []
    for row in rows:
        # print(row['Share Passport Photo (>1MB)'].split("id=")[1])
        img = get_image(row['Share Passport Photo (>1MB)'].split("id=")[1])
        images_list.append(img)

    print("Encoding Started ....")
    encode_list_known = find_encodings(images_list)
    print("Encoding Completed .....")


