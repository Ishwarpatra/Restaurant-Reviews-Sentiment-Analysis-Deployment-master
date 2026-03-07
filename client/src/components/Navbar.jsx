import React from 'react';

const Navbar = () => {
  return (
    <nav className="app-navbar">
      <a href="/" className="nav-brand">
        <span className="nav-brand-icon">
          <svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <linearGradient id="nav-icon-grad" x1="4" y1="4" x2="36" y2="36" gradientUnits="userSpaceOnUse">
                <stop offset="0%" stopColor="#F59E0B" />
                <stop offset="100%" stopColor="#F97316" />
              </linearGradient>
            </defs>
            <rect width="40" height="40" rx="10" fill="url(#nav-icon-grad)" opacity="0.12" />
            <rect width="40" height="40" rx="10" stroke="url(#nav-icon-grad)" strokeWidth="1.2" fill="none" opacity="0.3" />
            {/* Fork */}
            <path d="M15 10v6c0 2 1.5 3 3 3v10" stroke="url(#nav-icon-grad)" strokeWidth="1.8" strokeLinecap="round" fill="none" />
            <path d="M13 10v4" stroke="url(#nav-icon-grad)" strokeWidth="1.5" strokeLinecap="round" />
            <path d="M17 10v4" stroke="url(#nav-icon-grad)" strokeWidth="1.5" strokeLinecap="round" />
            {/* Knife */}
            <path d="M25 10c0 0 3 2 3 8v1h-3V29" stroke="url(#nav-icon-grad)" strokeWidth="1.8" strokeLinecap="round" fill="none" />
          </svg>
        </span>
        <span className="nav-brand-text">
          <span className="nav-brand-title">Sentiment Analyser</span>
          <span className="nav-brand-subtitle">AI-Powered Review Analysis</span>
        </span>
      </a>

      <div className="nav-right">
        <span className="nav-badge">v2.0</span>
        <span className="nav-status">
          <span className="nav-status-dot" />
          Live
        </span>
      </div>
    </nav>
  );
};

export default Navbar;