import React, { useState } from 'react';

function Register({ onRegister, onSwitchView }) {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Используем переменную окружения
      const apiUrl = process.env.REACT_APP_API_URL;
      const response = await fetch(`${apiUrl}/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, password }),
      });
      const data = await response.json();
      console.log("Server response:", data);  // Логируем ответ
      if (!response.ok) throw new Error(data.error || 'Registration failed');

      // Вызываем колбэк onRegister
      if (onRegister) onRegister(data.user);
    } catch (err) {
      setError('Registration failed: ' + err.message); // Вывод ошибки
    }
  };

  return (
    <div>
      <h2>Register</h2>
      {error && <p>{error}</p>}
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">Register</button>
      </form>
      <button onClick={onSwitchView}>Already have an account?</button>
    </div>
  );
}

export default Register;