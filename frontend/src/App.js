import React from 'react';
import { Routes, Route, Link, Navigate } from 'react-router-dom';
import HomePage from './pages/HomePage';
import SponsorLeaderboard from './pages/SponsorLeaderboard';
import Header from './components/Header';
import './App.css';

function App() {
  console.log("App component loaded.");

  return (
    <div className="App">
      <Header />
      <nav className="tab-nav">
        <Link to="/" className="tab-link">Home</Link>
        <Link to="/sponsor1" className="tab-link">Sponsor 1 Leaderboard</Link>
        <Link to="/sponsor2" className="tab-link">Sponsor 2 Leaderboard</Link>
      </nav>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/sponsor1" element={<SponsorLeaderboard sponsor="sponsor1" />} />
        <Route path="/sponsor2" element={<SponsorLeaderboard sponsor="sponsor2" />} />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </div>
  );
}

export default App;
