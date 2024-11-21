import cv2
import pytesseract
import json

# Update the Tesseract path as needed
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Pai\Desktop\TeamServay\tesseract_cmd\tesseract.exe"

def capture_id_card():

    cap = cv2.VideoCapture(0)
    print("Press 'S' to save image or 'Q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to open camera.")
            break

        cv2.imshow("ID Card Detector", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("s"):
            cv2.imwrite("id_card_for_cam.jpg", frame)
            print("Image saved successfully.")
            break
        elif key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

def crop_predefined_rois(image_path, rois):

    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError("Image could not be read. Please provide a valid image.")

    img = cv2.resize(img, (600, 400))
    cropped_images = {}

    for key, (x, y, w, h) in rois.items():
        if 0 <= x < img.shape[1] and 0 <= y < img.shape[0] and x + w <= img.shape[1] and y + h <= img.shape[0]:
            cropped_images[key] = img[y:y+h, x:x+w]
        else:
            print(f"Invalid ROI for {key}: {x, y, w, h}")
    
    return cropped_images

def enhance_and_extract_text(cropped_images, roi_langs):

    extracted_texts = {}

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    for key, img in cropped_images.items():
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        enhanced_img = clahe.apply(gray)
        extracted_texts[key] = pytesseract.image_to_string(enhanced_img, lang=roi_langs[key]).strip()
    
    return extracted_texts

def clean_extracted_text(extracted_texts):

    return {key: text.replace(" ", "") for key, text in extracted_texts.items()}

def save_to_json(data, filename="id_card_data.json"):

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    print(f"Data saved to {filename} successfully.")

if __name__ == "__main__":
    
    # Predefined ROIs (x, y, width, height)
    rois = {
        "id_num": (255, 45, 300, 35),
        "name_th": (168, 88, 400, 42),
        "name_eng": (240, 126, 350, 35),
        "surname_eng": (269, 153, 320, 30),
        "address": (50, 242, 400, 57),
    }
    
    # Languages for each ROI
    roi_langs = {
        "id_num": "eng",
        "name_th": "tha",
        "name_eng": "eng",
        "surname_eng": "eng",
        "address": "tha",
    }

    image_num = input("Enter image number: ")
    image_path = f"C:\\Users\\Pai\\Desktop\\TeamServay\\ID_card\\IDcard{image_num}.jpg"

    print(f"Processing ID card {image_num}...")

    # Extract and process text
    try:
        cropped_images = crop_predefined_rois(image_path, rois)
        extracted_texts = enhance_and_extract_text(cropped_images, roi_langs)
        cleaned_texts = clean_extracted_text(extracted_texts)

        # Display the extracted data
        for key, text in cleaned_texts.items():
            print(f"{key.capitalize()}: {text}")

        # Save data to JSON
        save_to_json(cleaned_texts)
    except Exception as e:
        print(f"Error: {e}")
