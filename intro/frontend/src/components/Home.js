import React, { useState, useEffect, useCallback } from 'react';

const Home = ({ user }) => {
  const [file, setFile] = useState(null);
  const [history, setHistory] = useState([]);
  const [error, setError] = useState('');
  const [result, setResult] = useState('');

  const fetchHistory = useCallback(async () => {
    try {
      const apiUrl = process.env.REACT_APP_API_URL;
      const response = await fetch(`${apiUrl}/history?user_id=${user.id}`);
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || 'Failed to fetch history');
      setHistory(data.history);
    } catch (err) {
      setError('Failed to load history: ' + err.message);
    }
  }, [user.id]);

  useEffect(() => {
    fetchHistory();
  }, [fetchHistory]);

  const handleFileUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a file');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('user_id', user.id);

    try {
      const apiUrl = process.env.REACT_APP_API_URL;
      const response = await fetch(`${apiUrl}/upload`, {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || 'File upload failed');

      setResult(data.text);
      setError('');
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