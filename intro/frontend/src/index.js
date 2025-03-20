import React from 'react';
import { createRoot } from 'react-dom/client'; // Используем createRoot для React 18
import App from './App'; 
import './App.css';

//тут корневой элемент и рендерим приложение
const container = document.getElementById('root');
const root = createRoot(container);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);