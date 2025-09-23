import React from 'react';
import './Header.css';

function Header() {
  return (
    <header className="app-header">
      <div className="header-left">
        <div className="njcu-logo">
          <img 
            src="https://www.njcu.edu/sites/default/files/styles/njcu_medium/public/njcu-logo-white.png" 
            alt="NJCU Logo" 
            className="logo-image"
            onError={(e) => {
              e.target.style.display = 'none';
              e.target.nextSibling.style.display = 'block';
            }}
          />
          <div className="logo-fallback" style={{display: 'none'}}>
            <span className="logo-text">NJCU</span>
          </div>
        </div>
        <div className="header-title">
          <h1>New Jersey City University</h1>
          <span className="subtitle">AI Student Assistant</span>
        </div>
      </div>
      <div className="header-right">
        <div className="header-actions">
          <button className="help-btn">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 17h-2v-2h2v2zm2.07-7.75l-.9.92C13.45 12.9 13 13.5 13 15h-2v-.5c0-1.1.45-2.1 1.17-2.83l1.24-1.26c.37-.36.59-.86.59-1.41 0-1.1-.9-2-2-2s-2 .9-2 2H8c0-2.21 1.79-4 4-4s4 1.79 4 4c0 .88-.36 1.68-.93 2.25z" fill="currentColor"/>
            </svg>
            Help
          </button>
          <div className="user-profile">
            <div className="avatar">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z" fill="currentColor"/>
              </svg>
            </div>
            <span className="username">Student</span>
          </div>
        </div>
      </div>
    </header>
  );
}

export default Header;