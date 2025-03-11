
import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import App from './App';
import Profile from './pages/Profile';
import Navbar from './components/Navbar';

ReactDOM.render(
    <Router>
        <Navbar />
        <Routes>
            <Route path="/" element={<App />} />
            <Route path="/profile" element={<Profile />} />
        </Routes>
    </Router>,
    document.getElementById('root')
);
