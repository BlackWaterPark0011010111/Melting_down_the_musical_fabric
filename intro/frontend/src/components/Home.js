import React, { useState } from 'react';
import '../App.css';

const Home = ({ user }) => {
  const [file, setFile] = useState(null);  // Для загруженного файла
  const [text, setText] = useState('');   // Для текста (результата анализа)
  const [error, setError] = useState(''); // Для ошибок

  // Обработка загрузки файла
  const handleFileUpload = async (event) => {
    const uploadedFile = event.target.files[0];
    if (!uploadedFile) {
      setError('Please select a file.');
      return;
    }

    setFile(uploadedFile);

    try {
      const formData = new FormData();
      formData.append('file', uploadedFile);

      // Отправляем файл на сервер для анализа
      const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const result = await response.json();
        setText(result.text);  // Устанавливаем текст (результат анализа)
        setError('');
      } else {
        const errorData = await response.json();
        setError(errorData.error || 'Failed to process the file.');
      }
    } catch (err) {
      setError('An error occurred while processing the file.');
    }
  };

  // Обработка скачивания текста в выбранном формате
  const handleDownload = async (format) => {
    if (!text) {
      setError('No text available to download.');
      return;
    }

    try {
      const response = await fetch(`http://localhost:5000/download/${format}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text }),
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `output.${format}`;
        a.click();
        window.URL.revokeObjectURL(url);
      } else {
        const errorData = await response.json();
        setError(errorData.error || 'Failed to download file.');
      }
    } catch (err) {
      setError('An error occurred while downloading the file.');
    }
  };

  return (
    <div className="App">
      <h1>Welcome, {user.name}!</h1>
      <div className="upload-section">
        <h2>Upload a File</h2>
        <input type="file" onChange={handleFileUpload} />
        {file && <p>Uploaded file: {file.name}</p>}
      </div>

      <div className="result-section">
        <h2>Result</h2>
        <textarea
          value={text}
          readOnly
          rows="10"
          cols="50"
          placeholder="Analyzed text will appear here..."
        />
      </div>

      <div className="download-section">
        <h2>Download Result</h2>
        <button onClick={() => handleDownload('pdf')}>Download as PDF</button>
        <button onClick={() => handleDownload('jpg')}>Download as JPG</button>
        <button onClick={() => handleDownload('png')}>Download as PNG</button>
      </div>

      {error && <p className="error">{error}</p>}
    </div>
  );
};

export default Home;