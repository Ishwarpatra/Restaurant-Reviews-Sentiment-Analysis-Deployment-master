import React from 'react';

const Footer = () => {
  return (
    <footer className="app-footer">
      <div className="footer-links">
        <a href="https://github.com/Ishwarpatra" target="_blank" rel="noopener noreferrer" aria-label="GitHub">
          <i className="fab fa-github"></i>
        </a>
        <a href="https://linkedin.com/" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn">
          <i className="fab fa-linkedin"></i>
        </a>
      </div>
      <p className="footer-text">
        &copy; {new Date().getFullYear()} Restaurant Sentiment Analyser &middot; Built with FastAPI &amp; React
      </p>
    </footer>
  );
};

export default Footer;