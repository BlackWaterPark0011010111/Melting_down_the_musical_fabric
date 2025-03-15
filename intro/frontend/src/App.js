/*import React, { useState } from 'react';
import './App.css';

const RegistrationForm = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://127.0.0.1:5000/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name, email }),
      });
      const data = await response.json();
      alert(data.message || data.error); // Показываем сообщение от сервера
    } catch (error) {
      console.error('Error:', error);
      alert('An error occurred while registering.');
    }
  };

  return (
    <div className="registration-form">
      <h2>Регистрация нового пользователя</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name">Имя:</label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <button type="submit">Зарегистрироваться</button>
      </form>
    </div>
  );
};

function App() {
  return (
    <div className="App">
      <h1>Music Tab Converter</h1>
      <RegistrationForm />
    </div>
  );
}

export default App;
*/

import React from 'react';
import RegistrationForm from './RegistrationForm'; // Импортируем компонент RegistrationForm
import './App.css'; // Импортируем стили

function App() {
  return (
    <div className="App">
      <h1>Music Tab Converter</h1>
      <RegistrationForm /> {/* Используем компонент RegistrationForm */}
    </div>
  );
}

export default App;