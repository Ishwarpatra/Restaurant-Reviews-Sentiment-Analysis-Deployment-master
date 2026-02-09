import React from 'react';

const Navbar = () => {
  return (
    <nav className="app-navbar">
      <a href="/" className="nav-brand">
        <span className="nav-brand-icon">
          <i className="fas fa-utensils"></i>
        </span>
        Sentiment Analyser
        <span className="nav-badge">AI Powered</span>
      </a>
    </nav>
  );
};

export default Navbar;