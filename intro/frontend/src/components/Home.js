import React, { useState, useEffect } from 'react';

const Home = () => {
  const [file, setFile] = useState(null); // Состояние для выбранного файла
  const [history, setHistory] = useState([]); // Состояние для истории загрузок
  const [error, setError] = useState(''); // Состояние для ошибок
  const [result, setResult] = useState(''); // Состояние для результата (распознанный текст)

  // Загрузка истории при монтировании компонента
  useEffect(() => {
    fetchHistory();
  }, []);

  // Функция для загрузки истории
  const fetchHistory = async () => {
    try {
      const apiUrl = process.env.REACT_APP_API_URL;
      const response = await fetch(`${apiUrl}/history?user_id=1`); // Замените 1 на реальный ID пользователя
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || 'Failed to fetch history');
      setHistory(data.history);
    } catch (err) {
      setError('Failed to load history: ' + err.message);
    }
  };

  // Обработчик загрузки файла
  const handleFileUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a file');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('user_id', 1); // Замените 1 на реальный ID пользователя

    try {
      const apiUrl = process.env.REACT_APP_API_URL;
      const response = await fetch(`${apiUrl}/upload`, {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || 'File upload failed');

      // Обновляем историю и отображаем результат
      fetchHistory();
      setResult(data.text); // Сохраняем распознанный текст
      setError(''); // Очищаем ошибки
    } catch (err) {
      setError('File upload failed: ' + err.message);
    }
  };

  return (
    <div className="home">
      <h1>Welcome to the Music Tab Converter!</h1>

      {/* Поле для загрузки файла */}
      <div className="upload-section">
        <h2>Upload a File</h2>
        {error && <p className="error">{error}</p>}
        <form onSubmit={handleFileUpload}>
          <input
            type="file"
            onChange={(e) => setFile(e.target.files[0])}
            required
          />
          <button type="submit">Upload</button>
        </form>
      </div>

      {/* Результат распознавания */}
      {result && (
        <div className="result-section">
          <h2>Recognition Result</h2>
          <pre>{result}</pre>
        </div>
      )}

      {/* История загрузок */}
      <div className="history-section">
        <h2>Upload History</h2>
        {history.length === 0 ? (
          <p>No files uploaded yet.</p>
        ) : (
          <ul>
            {history.map((item) => (
              <li key={item.id}>
                <strong>{item.file_name}</strong> - {item.text}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default Home;