import React from 'react';
import { createRoot } from 'react-dom/client'; // Используем createRoot для React 18
import App from './App'; // Импортируем компонент App
import './App.css'; // Импортируем стили

// Создаём корневой элемент и рендерим приложение
const container = document.getElementById('root');
const root = createRoot(container); // Используем createRoot для React 18
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);