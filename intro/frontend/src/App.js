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
import Upload from './components/Upload';
import History from './components/History';
import './App.css';

function App() {
  const [user, setUser] = useState(null);
  const [view, setView] = useState('login');

  const handleLogin = (userData) => {
    setUser(userData);
    setView('upload');
  };

  const handleLogout = () => {
    setUser(null);
    setView('login');
  };

  return (
    <div className="App">
      <h1>Music Tab Converter</h1>
      {!user ? (
        view === 'login' ? (
          <Login onLogin={handleLogin} onSwitchView={() => setView('register')} />
        ) : (
          <Register onRegister={handleLogin} onSwitchView={() => setView('login')} />
        )
      ) : (
        <div>
          <button onClick={handleLogout}>Logout</button>
          <Upload userId={user.id} />
          <History userId={user.id} />
        </div>
      )}
    </div>
  );
}

export default App;