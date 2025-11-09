import React from 'react';
import './Header.css';

function Header({ searchTerm, onSearchChange }) {
  return (
    <header className="header">
      <div className="header-container">
        <div className="header-logo">
          <img src="/images/logo.svg" alt="Fan Gallery" />
          <h1>Fan Gallery</h1>
        </div>

        <div className="header-search">
          <input
            type="text"
            placeholder="캐릭터 이름으로 검색..."
            value={searchTerm}
            onChange={(e) => onSearchChange(e.target.value)}
            className="search-input"
          />
          <svg
            className="search-icon"
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
          >
            <circle cx="11" cy="11" r="8" />
            <path d="m21 21-4.35-4.35" />
          </svg>
        </div>
      </div>
    </header>
  );
}

export default Header;
