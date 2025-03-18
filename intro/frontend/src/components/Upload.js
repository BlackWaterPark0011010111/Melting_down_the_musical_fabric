import React, { useState } from 'react';
import { uploadFile } from '../api';

function Upload({ userId }) {
  const [file, setFile] = useState(null);
  const [text, setText] = useState('');
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a file');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('user_id', userId);

    try {
      const result = await uploadFile(formData);
      setText(result.text);
    } catch (err) {
      setError('File upload failed');
    }
  };

  return (
    <div>
      <h2>Upload File</h2>
      {error && <p>{error}</p>}
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} required />
        <button type="submit">Upload</button>
      </form>
      {text && (
        <div>
          <h3>Extracted Text:</h3>
          <pre>{text}</pre>
        </div>
      )}
    </div>
  );
}

export default Upload;