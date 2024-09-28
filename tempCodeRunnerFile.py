
    return text

def ocr_from_pdf(pdf_path):
    """Convert a PDF to images and perform OCR on each image."""
    images = convert_from_path(pdf_path)
    extracted_text = ""
    for img in images:
        extracted_text += perform_ocr(img) + "\n"
    return extracted_text

def recognize_food_image(food_image):
    """Recognize food in the uploaded image using the trained model."""