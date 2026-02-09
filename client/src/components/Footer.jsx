import React from 'react';

const Footer = () => {
  return (
    <footer className="footer mt-auto py-3 bg-light">
      <div className="container text-center">
        <div className="mb-2">
          <a href="#" className="text-decoration-none me-3"><i className="fab fa-github fa-lg contact-icon"></i></a>
          <a href="#" className="text-decoration-none"><i className="fab fa-linkedin fa-lg contact-icon"></i></a>
        </div>
        <p className="mb-0 text-muted">Made with ❤️ by You.</p>
      </div>
    </footer>
  );
};

export default Footer;