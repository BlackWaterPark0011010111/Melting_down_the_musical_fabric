import React, { useState } from 'react';
import axios from 'axios';
import './styles.css';

// Компонент RegistrationForm
const RegistrationForm = () => {
  console.log("RegistrationForm is rendering!"); // Проверка рендеринга
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    alert(`Регистрация успешна!\nИмя: ${name}\nEmail: ${email}`);
    setName('');
    setEmail('');
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
      <RegistrationForm /> {/* Использование компонента RegistrationForm */}
    </div>
  );
}

export default App;