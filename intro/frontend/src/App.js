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
import React, { useState } from 'react';
import Login from './components/Login';
import Register from './components/Register';
import Home from './components/Home'; 
import './App.css';

function App() {
  // Состояние для текущей страницы
  const [currentPage, setCurrentPage] = useState('login');

  // при успешного входа
  const handleLoginSuccess = (user) => {
    setCurrentPage('home'); // Переход на главную страницу после входа
  };

  // Обработчик успешной регистрации
  const handleRegisterSuccess = (user) => {
    setCurrentPage('home'); // Переход на главную страницу после регистрации
  };

  // Переход на страницу регистрации
  const handleSwitchToRegister = () => {
    setCurrentPage('register');
  };

  // Переход на страницу входа
  const handleSwitchToLogin = () => {
    setCurrentPage('login');
  };

  return (
    <div className="App">
      {/* Условный рендеринг на основе currentPage */}
      {currentPage === 'login' && (
        <Login
          onLogin={handleLoginSuccess}
          onSwitchView={handleSwitchToRegister}
        />
      )}
      {currentPage === 'register' && (
        <Register
          onRegister={handleRegisterSuccess}
          onSwitchView={handleSwitchToLogin}
        />
      )}
      {currentPage === 'home' && <Home />}
    </div>
  );
}

export default App;