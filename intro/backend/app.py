from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import bcrypt
from music21 import converter, stream
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

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(hashed_password, user_password):
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_password)
def init_db():
    with app.app_context():
        db = get_db_connection()
        cursor = db.cursor()

        # Создаем таблицу users, если она не существует
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')

        # Создаем таблицу translations, если она не существует
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

        db.commit()  # Фиксируем изменения
        cursor.close()  # Закрываем курсор # Закрываем курсор

# Инициализация базы данных
init_db()

# Маршрут для регистрации пользователя
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    print("Received data:", data)  # Логируем данные
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({"error": "Name, email, and password are required"}), 400

    try:
        db = get_db_connection()
        cursor = db.cursor()

        # Проверяем, существует ли пользователь с таким email
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        if user:
            return jsonify({"error": "User with this email already exists"}), 400

        # Хешируем пароль
        hashed_password = hash_password(password)

        # Сохраняем пользователя в базу данных
        cursor.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', (name, email, hashed_password))
        db.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        print("Error during registration:", str(e))  # Логируем ошибку
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()

# Маршрут для входа в систему
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    try:
        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Проверяем пароль
        if check_password(user['password'], password):
            return jsonify({"message": "Login successful", "user": {"id": user['id'], "name": user['name'], "email": user['email']}}), 200
        else:
            return jsonify({"error": "Invalid password"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()

# Маршрут для загрузки файла
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
            # Преобразуем файл в MusicXML (если это не MusicXML)
            if file.filename.endswith('.musicxml'):
                score = converter.parse(file_path)
            else:
                # Здесь можно добавить логику для обработки изображений/PDF
                raise Exception("Unsupported file format")

            # Преобразуем ноты в табулатуру
            tab_stream = stream.Stream()
            for part in score.parts:
                for note_or_chord in part.flat.notes:
                    if note_or_chord.isNote:
                        tab_stream.append(note_or_chord)
                    elif note_or_chord.isChord:
                        for n in note_or_chord.notes:
                            tab_stream.append(n)

            # Экспортируем табулатуру в текстовый формат
            tabs = tab_stream.write('text')
            return jsonify({"text": tabs})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)

    return jsonify({"error": "File processing failed"}), 500
# Маршрут для получения истории переводов
@app.route('/history', methods=['GET'])
def get_history():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM translations WHERE user_id = ? ORDER BY created_at DESC', (user_id,))
        translations = cursor.fetchall()
        return jsonify({"history": [dict(row) for row in translations]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()

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