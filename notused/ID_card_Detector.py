import cv2
import pytesseract

# ตั้งค่า path ของ Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Pai\Desktop\TeamServay\tesseract_cmd\tesseract.exe"  

def capture_id_card():
    cap = cv2.VideoCapture(1)
    print("กด 's' เพื่อบันทึกภาพ หรือ 'q' เพื่อออก")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("ไม่สามารถเปิดกล้องได้")
            break

        if frame is not None:
            print("Frame captured successfully")
        else:
            print("No frame captured")

        cv2.imshow("ID Card Detector", frame)

        print("Waiting for key press...")

        key = cv2.waitKey(0) & 0xFF
        if key == ord("s"):
            cv2.imwrite("id_card.jpg", frame)
            print("Image Saved Successfully")
            print(f"Key pressed: {key}")
            break

        elif key == ord("q"):
            print(f"Key pressed: {key}")
            break

    cap.release()
    cv2.destroyAllWindows()

def extract_text_from_image(image_path):
    img = cv2.imread(image_path)
    text = pytesseract.image_to_string(img, lang="tha+eng")  
    return text

def save_text_to_file(text, filename="id_card_data6.txt"):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)
    print(f"บันทึกข้อมูลในไฟล์ {filename} เรียบร้อย")

if __name__ == "__main__":
    capture_id_card()

    extracted_text = extract_text_from_image(r"C:\Users\Pai\Desktop\TeamServay\ID_card\IDcard6.jpg")
    print("ข้อมูลที่ดึงได้:\n", extracted_text)

    save_text_to_file(extracted_text)
