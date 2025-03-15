from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import os
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# Настройка пути к Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return "Welcome to the Music Tab Converter API!"

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        # Сохраняем файл
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Обработка PDF или изображения
        try:
            if file.filename.endswith('.pdf'):
                images = convert_from_path(file_path)
                text = ""
                for image in images:
                    text += pytesseract.image_to_string(image)
            else:
                image = Image.open(file_path)
                text = pytesseract.image_to_string(image)

            # Возвращаем распознанный текст
            return jsonify({"text": text})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            # Удаляем файл после обработки
            if os.path.exists(file_path):
                os.remove(file_path)

    return jsonify({"error": "File processing failed"}), 500

if __name__ == '__main__':
    app.run(debug=True)