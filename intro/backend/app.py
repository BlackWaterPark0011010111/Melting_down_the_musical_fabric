from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
from PIL import Image
import pytesseract
from pdf2image import convert_from_path

app = Flask(__name__)
CORS(app)

# Настройка пути к Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Папка для загрузки файлов
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Подключение к базе данных SQLite
DATABASE = 'users.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with app.app_context():
        db = get_db_connection()
        db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
        ''')
        db.commit()

# Инициализация базы данных
init_db()

# Маршрут для регистрации пользователя
@app.route('/register', methods=['POST'])  # Убедитесь, что methods=['POST']
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400

    try:
        db = get_db_connection()
        # Проверяем, существует ли пользователь с таким email
        user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        if user:
            return jsonify({"error": "User with this email already exists"}), 400

        # Сохраняем пользователя в базу данных
        db.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
        db.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

# Маршрут для загрузки файла
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