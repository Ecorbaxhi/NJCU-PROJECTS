import React from 'react';
import './Sidebar.css';

function Sidebar({ open, setOpen }) {
  return (
    <div className={`sidebar${open ? '' : ' collapsed'}`}>
      <div className="sidebar-header">
        <button className="collapse-btn" onClick={() => setOpen(!open)}>
          {open ? '<' : '>'}
        </button>
        {open && <h2 className="njcu-title">NJCU Chatbot</h2>}
      </div>
      <div className="sidebar-content">
        {open && (
          <ul className="sidebar-menu">
            <li>Home</li>
            <li>FAQ</li>
            <li>Contact</li>
          </ul>
        )}
      </div>
      <div className="sidebar-footer">
        <div className="user-section">
          <button className="login-btn">Login</button>
          {open && <div className="profile">Profile</div>}
        </div>
      </div>
    </div>
  );
}

export default Sidebar;