from flask import Flask, request, jsonify, render_template, session
import requests
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import json
from config import GEMINI_API_KEY, GEMINI_API_URL
from fastai.vision.all import load_learner, PILImage

# Recognize food image
def label_func(x):
    return x.parent.name

learn = load_learner("model.pkl")
labels = learn.dls.vocab

def predict(img):
    img = PILImage.create(img)
    pred, pred_idx, probs = learn.predict(img)

    # Get the index of the maximum probability
    max_prob_index = probs.argmax()

    # Return the label with the maximum probability and its value
    return {labels[max_prob_index]: float(probs[max_prob_index])}

app = Flask(__name__)
app.secret_key = 'cee0d5eadada6814a76ceae1eabb1922'

def perform_ocr(image):
    """Perform OCR on a single image using pytesseract."""
    text = pytesseract.image_to_string(image)
    return text

def ocr_from_pdf(pdf_path):
    """Convert a PDF to images and perform OCR on each image."""
    images = convert_from_path(pdf_path)
    extracted_text = ""
    for img in images:
        extracted_text += perform_ocr(img) + "\n"
    return extracted_text

def parse_with_gemini(text):
    """Use the Gemini API to parse text into a structured format."""
    # Create the prompt for the Gemini API
    prompt = f'Tabulate the following medicine data into a 3-column table: no other data should be given in output other than the table\n{text}'
    
    url = f"{GEMINI_API_URL}/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()  # Return the parsed JSON data
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/continue', methods=['POST'])
def continue_page():
    parsed_data = session.get('parsed_data', {})
    edited_data = request.form.get('edited_data', {})  # Get the edited data from the form
    session['edited_data'] = edited_data  # Save it for later use
    
    # Check if edited data is provided
    if edited_data:
        # Create the edited data structure
        edited_data_dict = {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {
                                "text": edited_data  # Use the edited data directly
                            }
                        ],
                        "role": "model"
                    },
                    "finishReason": "STOP",
                    "index": 0,
                    "safetyRatings": [
                        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "probability": "NEGLIGIBLE"},
                        {"category": "HARM_CATEGORY_HATE_SPEECH", "probability": "NEGLIGIBLE"},
                        {"category": "HARM_CATEGORY_HARASSMENT", "probability": "NEGLIGIBLE"},
                        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "probability": "LOW"}
                    ]
                }
            ],
            "usageMetadata": {
                "promptTokenCount": 1744,  # Example values; replace as needed
                "candidatesTokenCount": 432,
                "totalTokenCount": 2176
            }
        }
        
        parsed_data = edited_data_dict
    
    # Deserialize the JSON string into a Python dictionary
    if isinstance(parsed_data, str) and parsed_data.strip():
        try:
            parsed_data = json.loads(parsed_data)
        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")
            return "Invalid JSON data", 400

    return render_template('continue.html', data=parsed_data)

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and process OCR and parsing."""
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    
    # Check if the file is a PDF or an image
    if file.content_type == 'application/pdf':
        # Save the PDF temporarily
        pdf_path = f'temp_{file.filename}'
        file.save(pdf_path)
        extracted_text = ocr_from_pdf(pdf_path)
    else:
        # Assume it's an image (JPEG, PNG, etc.)
        image = Image.open(file.stream)  # Use stream to open the image directly
        extracted_text = perform_ocr(image)

    # Use Gemini API to tabulate the data
    parsed_data = parse_with_gemini(extracted_text)
    session['parsed_data'] = json.dumps(parsed_data)
    
    return render_template('results.html', data=parsed_data)

@app.route('/process', methods=['POST'])
def process_input():
    parsed_data = session.get('edited_data', {})
    if not parsed_data:
        parsed_data = session.get('parsed_data', {})
        if isinstance(parsed_data, str) and parsed_data.strip():
            try:
                parsed_data = json.loads(parsed_data)
            except json.JSONDecodeError as e:
                print(f"JSON decoding error: {e}")
                return "Invalid JSON data", 400
        
    food_image = request.files.get('food_image')
    food_description = request.form.get('food_description')
    ingredients_image = request.files.get('ingredients_image')

    # Initialize storage for OCR results
    ocr_results = {}

    # Check for food image
    if food_image:
        food_name = predict(food_image)
        ocr_results['food_name'] = food_name

    # Check for food description
    if food_description:
        ocr_results['food_description'] = food_description

    # Check for ingredients image
    if ingredients_image:
        image = Image.open(io.BytesIO(ingredients_image.read()))
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        ingredients_text = perform_ocr(image)
        ocr_results['ingredients_text'] = ingredients_text
    
    session['food_name'] = ocr_results
    return render_template('final_results.html', data=parsed_data, ocr_results=ocr_results)

@app.route('/generate-report', methods=['POST'])
def generate_report():
    disease = request.form.get('disease')
    allergies = request.form.get('allergies')
    food_name = session.get('food_name', {})
    parsed_meds = session.get('edited_data', {})
    
    report = report_gen(disease, allergies, food_name, parsed_meds)
    report_text = report['candidates'][0]['content']['parts'][0]['text']
    
    return render_template('report.html', report=report_text)

def report_gen(disease, allergies, food_name, parsed_meds):
    """Use the Gemini API to parse text into a structured format."""
    prompt = f"""
    Based on the following data, generate a report with the following:
    1. Food name: {food_name}
    2. Disease: {disease}
    3. Allergies: {allergies}
    4. MEDS: {parsed_meds}

    - Nutrition value of the food
    - Interactions of the food with medications (tabulated)
    - If allergic, suggest alternatives with similar nutrition values (tabulated)
    - Feedback on the user's diet (in bullet points)
    """
    
    url = f"{GEMINI_API_URL}/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

if __name__ == '__main__':
    app.run(debug=True)
