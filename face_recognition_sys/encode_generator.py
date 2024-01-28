import cv2
import face_recognition
import pickle

from get_drive_image_from_sheet import get_image, get_sheet_values, update_to_drive

SPREADSHEET_ID = "14SobbZCDKX9IKOJjY56G-WIOfVc7BctskqEKRG2ImAo"


def find_encodings(images_list):
    # print(images_list)
    encode_list = []
    for index, img in enumerate(images_list):
        print(index)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # print(face_recognition.face_encodings(img))
        face_loc = face_recognition.face_locations(img)
        face_encode = face_recognition.face_encodings(img, face_loc)
        if len(face_encode) > 0:
            encode = face_encode[0]
            encode_list.append(encode)
        else:
            print("Error at index: ", index)
    print(encode_list)
    return encode_list


def save_model(encode_list_known):
    print("Saving Encoded model....")
    file = open("EncodeFile.p", "wb")
    pickle.dump(encode_list_known, file)
    file.close()


def main():
    rows = get_sheet_values(SPREADSHEET_ID)
    images_list = []
    name_list = []
    for row in rows:
        # print(row['Share Passport Photo (>1MB)'].split("id=")[1])
        print(row)
        img = get_image(row['Share Passport Photo (>1MB)'].split("id=")[1])
        # print(img)
        images_list.append(img)
        name_list.append(row['Name'])

    print(name_list)

    print("Encoding Started ....")
    encode_list_known = find_encodings(images_list)
    print("Encoding Completed .....")
    # print(encode_list_known)

    encode_list_known_with_names = [encode_list_known, name_list]

    # print("Saving Encoded Model Started ....")
    # save_model(encode_list_known_with_names)
    # print("Saving Encoded Model Completed .....")

    print("Uploading Encoded Model Started ....")
    update_to_drive(encode_list_known_with_names)
    print("Uploaded Encoded Model Completed .....")

if __name__ == '__main__':
    main()
