import cv2
import pytesseract
import json
import re

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Pai\Desktop\TeamServay\tesseract_cmd\tesseract.exe"

def preprocess_image(image_path):

    img = cv2.imread(image_path)
    img = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    dilated = cv2.dilate(blurred, kernel, iterations=1)

    _, thresh = cv2.threshold(dilated, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    return thresh

def capture_id_card():
    cap = cv2.VideoCapture(0)
    print("Press 'S' to save image or 'Q' to quit")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Open camera failed")
            break

        cv2.imshow("ID Card Detector", frame)

        key = cv2.waitKey(0) & 0xFF
        if key == ord("s"):
            cv2.imwrite("id_card_for_cam.jpg", frame)
            print("Image Saved Successfully")
            break
        elif key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

def extract_text_from_image(image_path):

    processed_img = preprocess_image(image_path)
    custom_config = r"--psm 4 --oem 1" 
    text = pytesseract.image_to_string(processed_img, lang="tha", config=custom_config)
    return text

def remove_extra_spaces(text):
    return text.replace(" ", "")

def save_data_to_text(text, filename="id_card_data.txt"):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)
    print(f"Save {filename} successfully")

def parse_data(text):
    data = {}

    # ID_number
    id_match = re.search(r"\s*([\d]{13})", text)
    data["ID_number"] = id_match.group(1) if id_match else None

    # Fullname_TH (adjusted to read Thai name after "ชื่อตัวและชื่อสกุล")
    name_th_match = re.search(r"ชื่อตัวและชื่อสกุล\s*(.*?)(?:\n|$)", text)
    data["Fullname_TH"] = name_th_match.group(1).strip() if name_th_match else None

    # Fullname_Eng (if needed, adjust similarly)
    name_eng_match = re.search(r"Name\s*(.*?)(?:\n|$)", text)
    lastname_eng_match = re.search(r"Lastname\s*(.*?)(?:\n|$)", text)

    if name_eng_match and lastname_eng_match:
        data["Fullname_Eng"] = f"{name_eng_match.group(1).strip()} {lastname_eng_match.group(1).strip()}"
    else:
        data["Fullname_Eng"] = None

    # Address
    address_match = re.search(r"ที่อยู่\s*(.*\n.*)", text)
    data["address"] = " ".join(address_match.groups()).replace("\n", " ").strip() if address_match else None

    return data

def save_data_to_json(data, filename="id_card_data.json"):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    print(f"Saved data to {filename} successfully")

if __name__ == "__main__":
    while True:
        choice = input("Press 'c' to open camera or 'i' to choose image : ").lower()
        if choice == 'c':
            capture_id_card()
            image_path = "id_card_for_cam.jpg"
            break
        elif choice == 'i':
            image_num = input("Enter image number : ") 
            image_path = f"C:\\Users\\Pai\\Desktop\\TeamServay\\ID_card\\IDcard{image_num}.jpg"
            print(f'Scanning from ID card number {image_num}')
            break

    extracted_data = extract_text_from_image(image_path)
    extracted_data = remove_extra_spaces(extracted_data)
    parsed_data = parse_data(extracted_data)
    print("Data Extracted:\n", parsed_data)
    save_data_to_json(parsed_data)
    save_data_to_text(extracted_data)
