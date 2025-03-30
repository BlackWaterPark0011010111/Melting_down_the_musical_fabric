from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import sqlite3
import os
from PIL import Image, ImageDraw, ImageFont
import pytesseract
from pdf2image import convert_from_path
import bcrypt
from music21 import stream, converter,  note, chord, meter, tempo
import pdfkit
from io import BytesIO
import cv2  # Для обработки изображений
import logging
from contextlib import closing

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

DATABASE = 'users.db'


wkhtmltopdf_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
if not os.path.exists(wkhtmltopdf_path):
    logger.error("wkhtmltopdf not found at the specified path: %s", wkhtmltopdf_path)
    raise FileNotFoundError("wkhtmltopdf not found at the specified path")

pdfkit_config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(hashed_password, user_password):
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password)

def init_db():
    with app.app_context():
        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS translations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                file_name TEXT NOT NULL,
                text TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        db.commit()  
        cursor.close()  

init_db()

def preprocess_image(image_path):
    try:
        image = cv2.imread(image_path)
        if image is None:
            logger.error("Failed to read the image file: %s", image_path)
            raise ValueError("Failed to read the image file")

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        gray = cv2.equalizeHist(gray)

        _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        sharpened = cv2.GaussianBlur(binary, (0, 0), 3)
        sharpened = cv2.addWeighted(binary, 1.5, sharpened, -0.5, 0)

        denoised = cv2.fastNlMeansDenoising(sharpened, h=10)

        return denoised
    except Exception as e:
        logger.error("Error during image preprocessing: %s", str(e))
        raise

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    logger.info("Received data: %s", data)  
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({"error": "Name, email, and password are required"}), 400

    try:
        with closing(get_db_connection()) as db:
            cursor = db.cursor()

            cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            user = cursor.fetchone()
            if user:
                return jsonify({"error": "User with this email already exists"}), 400

            hashed_password = hash_password(password)

            cursor.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', (name, email, hashed_password))
            db.commit()
            return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        logger.error("Error during registration: %s", str(e))  
        return jsonify({"error": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    try:
        with closing(get_db_connection()) as db:
            cursor = db.cursor()

            cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            user = cursor.fetchone()
            if not user:
                return jsonify({"error": "User not found"}), 404

            if check_password(user['password'], password):
                return jsonify({"message": "Login successful", "user": {"id": user['id'], "name": user['name'], "email": user['email']}}), 200
            else:
                return jsonify({"error": "Invalid password"}), 401
    except Exception as e:
        logger.error("Error during login: %s", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        try:
            mime_type = file.content_type
            logger.info("Uploaded file MIME type: %s", mime_type)

            if file.filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                if not os.path.exists(file_path):
                    return jsonify({"error": "File does not exist"}), 400

                processed_image = preprocess_image(file_path)

                text = pytesseract.image_to_string(processed_image, lang='eng+rus', config='--psm 6 --oem 3')
                return jsonify({"text": text})
            elif file.filename.endswith('.musicxml'):
                score = converter.parse(file_path)
                tab_stream = stream.Stream()
                for part in score.parts:
                    for note_or_chord in part.flat.notes:
                        if note_or_chord.isNote:
                            tab_stream.append(note_or_chord)
                        elif note_or_chord.isChord:
                            for n in note_or_chord.notes:
                                tab_stream.append(n)
                tabs = tab_stream.write('text')
                return jsonify({"text": tabs})
            else:
                return jsonify({"error": "Unsupported file format"}), 400
        except Exception as e:
            logger.error("Error during file processing: %s", str(e))
            return jsonify({"error": str(e)}), 500
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)

    return jsonify({"error": "File processing failed"}), 500

@app.route('/history', methods=['GET'])
def get_history():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    try:
        with closing(get_db_connection()) as db:
            cursor = db.cursor()
            cursor.execute('SELECT * FROM translations WHERE user_id = ? ORDER BY created_at DESC', (user_id,))
            translations = cursor.fetchall()
            return jsonify({"history": [dict(row) for row in translations]})
    except Exception as e:
        logger.error("Error fetching history: %s", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/download/pdf', methods=['POST'])
def download_pdf():
    data = request.get_json()
    text = data.get('text')

    if not text:
        return jsonify({"error": "Text is required"}), 400

    try:
        pdf = pdfkit.from_string(text, False, configuration=pdfkit_config)

        return send_file(
            BytesIO(pdf),
            mimetype='application/pdf',
            as_attachment=True,
            download_name='output.pdf'
        )
    except Exception as e:
        logger.error("Error generating PDF: %s", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/download/jpg', methods=['POST'])
def download_jpg():
    data = request.get_json()
    text = data.get('text')

    if not text:
        return jsonify({"error": "Text is required"}), 400

    try:
        image = Image.new('RGB', (800, 600), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        draw.text((10, 10), text, fill="black", font=font)

        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)

        return send_file(
            img_byte_arr,
            mimetype='image/jpeg',
            as_attachment=True,
            download_name='output.jpg'
        )
    except Exception as e:
        logger.error("Error generating JPG: %s", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/download/png', methods=['POST'])
def download_png():
    data = request.get_json()
    text = data.get('text')

    if not text:
        return jsonify({"error": "Text is required"}), 400

    try:
        image = Image.new('RGB', (800, 600), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        draw.text((10, 10), text, fill="black", font=font)

        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        return send_file(
            img_byte_arr,
            mimetype='image/png',
            as_attachment=True,
            download_name='output.png'
        )
    except Exception as e:
        logger.error("Error generating PNG: %s", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/routes')
def list_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            "endpoint": rule.endpoint,
            "methods": list(rule.methods),
            "path": rule.rule
        })
    return jsonify(routes)

@app.route('/')
def home():
    return "Welcome to the Music Tab Converter API!"

if __name__ == '__main__':
    app.run(debug=True, port=5000)