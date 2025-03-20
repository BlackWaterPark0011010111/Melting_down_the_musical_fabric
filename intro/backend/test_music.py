from music21 import converter

# Исправленный путь к файлу
score = converter.parse(r'C:\Users\roxfo\Desktop\MySnake\Python\example.musicxml')

# Отображение нот
score.show()