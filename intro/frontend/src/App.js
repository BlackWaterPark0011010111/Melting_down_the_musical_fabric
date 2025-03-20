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
*/import React, { useState } from 'react';
import Login from './components/Login';
import Register from './components/Register';
import Home from './components/Home'; 
import './App.css';

function App() {
  const [currentPage, setCurrentPage] = useState('login'); // текущая страница
  const [user, setUser] = useState(null); //хранения данных пользователя

 
  const handleLoginSuccess = (userData) => {
    setUser(userData); //сохранение данных юзера
    setCurrentPage('home'); //переход на main page
  };

  //при успешной регистрации
  const handleRegisterSuccess = (userData) => {
    setUser(userData); //сохраняем  юзера
    setCurrentPage('home'); //переход на главную 
  };

  
  const handleSwitchToRegister = () => {//переход на регистрацию
    setCurrentPage('register');
  };


  const handleSwitchToLogin = () => {  //переход на вход
    setCurrentPage('login');
  };

  return (
    <div className="App">
      {/*рендеринг на currentPage */}
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
      {currentPage === 'home' && <Home user={user} />}
    </div>
  );
}

export default App;