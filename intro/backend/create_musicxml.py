from music21 import stream, note, meter, clef

# Создаем новый поток (партитуру)
score = stream.Score()

# Добавляем метру (4/4)
score.append(meter.TimeSignature('4/4'))

# Добавляем скрипичный ключ
score.append(clef.TrebleClef())

# Создаем ноты
notes = [
    note.Note("C4", quarterLength=1.0),  # До (C) четвертой октавы, длительность 1.0
    note.Note("D4", quarterLength=1.0),  # Ре (D) четвертой октавы, длительность 1.0
    note.Note("E4", quarterLength=1.0),  # Ми (E) четвертой октавы, длительность 1.0
    note.Note("F4", quarterLength=1.0),  # Фа (F) четвертой октавы, длительность 1.0
]

# Добавляем ноты в поток
for n in notes:
    score.append(n)

# Экспортируем в MusicXML
score.write('musicxml', fp='example.musicxml')

print("Файл example.musicxml успешно создан!")

