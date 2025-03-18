const API_URL = 'http://localhost:5000';

export const login = async (email, password) => {
  const response = await fetch(`${API_URL}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error);
  return data.user;
};

export const register = async (name, email, password) => {
    const response = await fetch(`${API_URL}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, password }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Registration failed');
    return data.user;
  };

export const uploadFile = async (formData) => {
  const response = await fetch(`${API_URL}/upload`, {
    method: 'POST',
    body: formData,
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error);
  return data;
};

export const getHistory = async (userId) => {
  const response = await fetch(`${API_URL}/history?user_id=${userId}`);
  const data = await response.json();
  if (!response.ok) throw new Error(data.error);
  return data.history;
};