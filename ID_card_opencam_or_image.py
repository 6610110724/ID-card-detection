import cv2
import pytesseract

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

def extract_text_from_image(image_path):
    img = cv2.imread(image_path)
    text = pytesseract.image_to_string(img, lang="tha+eng")  
    return text

def save_text_to_file(text, filename="id_card_data.txt"):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)
    print(f"Save {filename} successfully")

def remove_extra_spaces(text):
    return text.replace(" ", "")


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

    extracted_data = extract_text_from_image(image_path)
    extracted_data = remove_extra_spaces(extracted_data)  
    print("Data Extracted :\n", extracted_data)
    save_text_to_file(extracted_data)

