import React, { useEffect, useState } from 'react';
import { getHistory } from '../api';

function History({ userId }) {
  const [history, setHistory] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const data = await getHistory(userId);
        setHistory(data);
      } catch (err) {
        setError('Failed to fetch history');
      }
    };

    fetchHistory();
  }, [userId]);

  return (
    <div>
      <h2>History</h2>
      {error && <p>{error}</p>}
      {history.length === 0 ? (
        <p>No history found.</p>
      ) : (
        <ul>
          {history.map((item) => (
            <li key={item.id}>
              <strong>{item.file_name}</strong>: {item.text}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default History;