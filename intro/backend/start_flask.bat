@echo off
set FLASK_APP=app.py
set FLASK_ENV=development
call "C:\Users\roxfo\miniconda3\Scripts\activate.bat" melting
python -m flask run --host=0.0.0.0 --port=5000
pause