import cv2
import pytesseract
import re
import json

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Pai\Desktop\TeamServay\tesseract_cmd\tesseract.exe"

def capture_id_card():
    cap = cv2.VideoCapture(1)
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
    img = cv2.imread(image_path)
    text = pytesseract.image_to_string(img, lang="tha+eng")
    return text

def parse_id_card_data(text):
    # Regular expression to find the ID number
    id_number_match = re.search(r'\b\d{1}-\d{4}-\d{5}-\d{2}-\d{1}\b|\b\d{13}\b', text)
    id_number = id_number_match.group().replace(" ", "") if id_number_match else ""

    # Separate lines for further analysis
    lines = text.splitlines()
    fullname_th = ""
    fullname_eng = ""
    address = ""

    # Identify potential names and address
    for line in lines:
        if re.search(r'[ก-๙]', line) and not fullname_th:
            fullname_th = line.strip()  # First Thai line as Thai full name
        elif re.search(r'[A-Za-z]', line) and not fullname_eng:
            fullname_eng = line.strip()  # First English line as English full name
        elif fullname_th and fullname_eng:
            address += line.strip() + " "  # Address starts accumulating after names

    # Package data as JSON
    data = {
        "ID_number": id_number,
        "Fullname_TH": fullname_th,
        "Fullname_Eng": fullname_eng,
        "address": address.strip()
    }
    return data

def save_data_to_json(data, filename="id_card_data.json"):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    print(f"Data saved to {filename} successfully")

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
            print(f'scanning from ID card number {image_num}')
            break

    # Extract and parse text data
    extracted_text = extract_text_from_image(image_path)
    parsed_data = parse_id_card_data(extracted_text)
    print("Data Extracted:\n", parsed_data)

    # Save data as JSON
    save_data_to_json(parsed_data)
