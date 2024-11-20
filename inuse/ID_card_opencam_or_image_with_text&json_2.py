import cv2
import pytesseract
import json
import re

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Pai\Desktop\TeamServay\tesseract_cmd\tesseract.exe" #อย่าลืมเปลี่ยน Path file

def capture_id_card():
    cap = cv2.VideoCapture(0)
    print("Press 'S' to save image or 'Q' to quit")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Open camera failed")
            break

        if frame is not None:
            print("Frame captured successfully")
        else:
            print("No frame captured")

        cv2.imshow("ID Card Detector", frame)
        print("Waiting for key press...")

        key = cv2.waitKey(0) & 0xFF
        if key == ord("s"):
            cv2.imwrite("id_card_for_cam.jpg", frame)
            print("Image Saved Successfully")
            break
        elif key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


def apply_clahe(image_path):

    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    assert img is not None, "Image could not be read. Please check the path."

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced_img = clahe.apply(img)

    cv2.imwrite("enhanced_image.jpg", enhanced_img)

    return enhanced_img


def extract_text_from_image(image_path):
    # Apply CLAHE enhancement
    enhanced_img = apply_clahe(image_path)

    # Use Tesseract OCR for text extraction
    text_th = pytesseract.image_to_string(enhanced_img, lang="tha")
    text_eng = pytesseract.image_to_string(enhanced_img, lang="eng")
    return text_th, text_eng



def remove_extra_spaces(text_th, text_eng):
    return text_th.replace(" ", ""), text_eng.replace(" ", "")


def save_data_to_text(text_th, text_eng, filename="id_card_data.txt"):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text_th + "\n" + text_eng)
    print(f"Saved {filename} successfully")


def parse_data(text_th, text_eng): 
    data = {}

    # ID_number 
    id_match = re.search(r"\s*([\d]{13})", text_eng)
    data["ID_number"] = id_match.group(1) if id_match else None

    # Fullname_TH
    name_th_match = re.search(r"ชื่อตัวและชื่อสกุล\s*(.*?)(?:\n)", text_th)
    data["Fullname_TH"] = name_th_match.group(1).strip() if name_th_match else None

    # Fullname_Eng 
    name_eng_match = re.search(r"Name\s*(.*?)(?:\n)", text_eng)
    lastname_eng_match = re.search(r"Lastname\s*(.*?)(?:\n)", text_eng)

    if name_eng_match and lastname_eng_match:
        data["Fullname_Eng"] = f"{name_eng_match.group(1).strip()} {lastname_eng_match.group(1).strip()}"
    else:
        data["Fullname_Eng"] = None

    # Address
    address_match = re.search(r"ที่อยู่\s*(.*\n.*)", text_th)
    data["address"] = " ".join(address_match.groups()).replace("\n", " ").strip() if address_match else None

    return data


def save_data_to_json(data, filename="id_card_data.json"):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    print(f"Saved data to {filename} successfully")


if __name__ == "__main__":
    
    while True:

        image_num = input("Enter image number : ") 
        image_path = f"C:\\Users\\Pai\\Desktop\\TeamServay\\ID_card\\IDcard{image_num}.jpg"
        print(f'Scanning from ID card number {image_num}')
        break


    text_th, text_eng = extract_text_from_image(image_path)
    text_th, text_eng = remove_extra_spaces(text_th, text_eng)
    parsed_data = parse_data(text_th, text_eng)

    print("Data Extracted:\n", parsed_data)
    save_data_to_json(parsed_data)
    save_data_to_text(text_th, text_eng)


