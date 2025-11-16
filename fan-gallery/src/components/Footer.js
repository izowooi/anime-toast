import React from 'react';
import { Link } from 'react-router-dom';
import './Footer.css';

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-container">
        <p className="footer-text">
          © 2024 Fan Gallery. 좋아하는 캐릭터들을 모아보세요.
        </p>
        <div className="footer-links">
          <Link to="/terms-of-service" className="footer-link">
            Terms of Service
          </Link>
          <span className="footer-link-separator">|</span>
          <Link to="/privacy-policy" className="footer-link">
            Privacy Policy
          </Link>
        </div>
        <p className="footer-subtext">
          Made with ❤️ for anime and game fans
        </p>
      </div>
    </footer>
  );
}

export default Footer;
