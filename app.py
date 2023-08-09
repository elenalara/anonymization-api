from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
import pytesseract
# from PIL import Image
import cv2
import spacy
import nltk
import re
import pydicom

app = Flask(__name__)

def has_only_non_alphanumeric_chars(s):
    """This function takes a string s as input and checks each character in the string. If any character is not alphanumeric, the function
    continues to the next character. If a character is alphanumeric, the function increments a count of alphanumeric characters. If the count
    exceeds 2, the function immediately returns False because there are more than two alphanumeric characters in the string. Otherwise, the
    function returns True.
    """
    if s:
        alphanumeric_count = 0
        for c in s:
            if c.isalnum():
                alphanumeric_count += 1
                if alphanumeric_count > 2:
                    return False
    return True

def replace_control_characters(text):
    """replace control character that are not allowed in CSV files.
    """
    csv_control_chars_pattern = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]')  # regular expression to match any control characters
    if text:
        return csv_control_chars_pattern.sub('', text)
    else:
        return None

def convertir_mayusculas(match):
    return match.group().lower().capitalize() # converts to lowercase and capitalizes the first letter

def detect_personal_info(text, nlp_models, names_list, language=['en', 'es', 'ca'], convert=False):
    if not text:
        return False
    
    #Preprocess text
    text = replace_control_characters(text)
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"\s+", " ", text) # Replace consecutive spaces with a single space
    
    # Search for patterns
    patterns = [
        r'\b\w{0,3}\d{6,8}[a-zA-Z]\b',  # ID numbers
        r'id\s*:\s*(\d+)',  # ID numbers
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Emails
        r'\b\w{4}\d{8,}\b'  # CIPs
    ]
    
    try:
        for pattern in patterns:
            matches = re.findall(pattern, text) # Search ID numbers
            if len(matches) > 0:
                return True
        
        if convert:
            text = re.sub(r'\b[A-Z]+\b', convertir_mayusculas, text)
        
        # NLTK
        sentences = nltk.sent_tokenize(text) # tokenize text into sentences and words
        words = [nltk.word_tokenize(sentence) for sentence in sentences]
        tagged_words = [nltk.pos_tag(word) for word in words] # tag words with their part of speech
        named_entities = nltk.ne_chunk_sents(tagged_words, binary=False) # recognize named entities in tagged words
        for sentence in named_entities:
            for chunk in sentence:
                if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
                    return True

        text = text.lower() # convert to lower case
        for word in text.split():
            if word in names_list:
                return True

        # Spacy            
        nlp_dict = {lang: nlp_models[lang] for lang in language}
        for nlp in nlp_dict.values():
            doc = nlp(text)
            for ent in doc.ents:
                if ent.label_ == "PERSON" or ent.label_ == "PER":
                    return True

    except Exception as e:
        return f"Error: {str(e)}"
    
    return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/main', methods=['POST'])

def main():
    try:
        image_file = request.files['image']

        # Check if the image is a DICOM image
        try:
            image = pydicom.dcmread(image_file)
            if isinstance(image, pydicom.dataset.FileDataset):
                if "PixelData" in image:
                    image = image.pixel_array
                else:
                    return jsonify({"error": "DICOM has no pixel data"}), 400
            else:
                return jsonify({"error": "Invalid DICOM dataset"}), 400
        except:
            # If not a DICOM image, assume it is a regular image format (PNG, JPG, etc.)
            try:
                image_file.seek(0)
                image = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
            except:
                return jsonify({"error": "Tipo de imagen no soportado"}), 400
        
        try:
            text = pytesseract.image_to_string(image)
            if not text.strip():
                text = None
            else:
                text = text.strip()
        except Exception as e:
            return jsonify({"error in text": str(e)}), 400

        if has_only_non_alphanumeric_chars(text):
            text = None

        names = pd.read_csv('util_data/list_names_cat.csv')
        names['n'] = names['n'].str.lower() # convert to lower case
        name_list = names['n'].tolist()
        name_list = [string.strip() for string in name_list]

        spacy.prefer_gpu()
        nlp_models = {}
        for lang in ['en', 'es', 'ca']:
            if lang == 'en':
                nlp_models[lang] = spacy.load(f"{lang}_core_web_sm", disable=['parser'])
            else:
                nlp_models[lang] = spacy.load(f"{lang}_core_news_sm", disable=['parser'])

        response = {"output": detect_personal_info(text, nlp_models, name_list, convert=True)}
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
