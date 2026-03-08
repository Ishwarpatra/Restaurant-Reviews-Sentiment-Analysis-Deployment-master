import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Menu, X } from 'lucide-react';

const Navbar = () => {
  const location = useLocation();
  const [mobileOpen, setMobileOpen] = useState(false);

  const isActive = (path) => location.pathname === path;

  const navLinks = [
    { to: '/', label: 'Home' },
    { to: '/analyze', label: 'Analyser' },
    { to: '/about', label: 'Tech Stack' },
  ];

  return (
    <nav className="app-navbar">
      {/* Brand */}
      <Link to="/" className="nav-brand" onClick={() => setMobileOpen(false)}>
        <span className="nav-brand-icon">
          <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
            <defs>
              <linearGradient id="nav-icon-grad" x1="4" y1="4" x2="36" y2="36" gradientUnits="userSpaceOnUse">
                <stop offset="0%" stopColor="#F59E0B" />
                <stop offset="100%" stopColor="#F97316" />
              </linearGradient>
            </defs>
            <rect width="40" height="40" rx="10" fill="url(#nav-icon-grad)" opacity="0.12" />
            <rect width="40" height="40" rx="10" stroke="url(#nav-icon-grad)" strokeWidth="1.2" fill="none" opacity="0.3" />
            <path d="M15 10v6c0 2 1.5 3 3 3v10" stroke="url(#nav-icon-grad)" strokeWidth="1.8" strokeLinecap="round" fill="none" />
            <path d="M13 10v4" stroke="url(#nav-icon-grad)" strokeWidth="1.5" strokeLinecap="round" />
            <path d="M17 10v4" stroke="url(#nav-icon-grad)" strokeWidth="1.5" strokeLinecap="round" />
            <path d="M25 10c0 0 3 2 3 8v1h-3V29" stroke="url(#nav-icon-grad)" strokeWidth="1.8" strokeLinecap="round" fill="none" />
          </svg>
        </span>
        <span className="nav-brand-text">
          <span className="nav-brand-title">Sentiment Analyser</span>
          <span className="nav-brand-subtitle">AI-Powered Review Analysis</span>
        </span>
      </Link>

      {/* Desktop Nav */}
      <div className="nav-center">
        {navLinks.map((link) => (
          <Link
            key={link.to}
            to={link.to}
            className={`nav-link-item ${isActive(link.to) ? 'active' : ''}`}
          >
            {link.label}
          </Link>
        ))}
      </div>

      {/* Right side */}
      <div className="nav-right">
        <span className="nav-badge">v2.0</span>
        <span className="nav-status">
          <span className="nav-status-dot" />
          Live
        </span>

        {/* Mobile toggle */}
        <button
          className="nav-mobile-toggle"
          onClick={() => setMobileOpen(!mobileOpen)}
          aria-label="Toggle navigation"
        >
          {mobileOpen ? <X size={22} /> : <Menu size={22} />}
        </button>
      </div>

      {/* Mobile Nav Overlay */}
      {mobileOpen && (
        <div className="nav-mobile-overlay">
          {navLinks.map((link) => (
            <Link
              key={link.to}
              to={link.to}
              className={`nav-mobile-link ${isActive(link.to) ? 'active' : ''}`}
              onClick={() => setMobileOpen(false)}
            >
              {link.label}
            </Link>
          ))}
        </div>
      )}
    </nav>
  );
};

export default Navbar;