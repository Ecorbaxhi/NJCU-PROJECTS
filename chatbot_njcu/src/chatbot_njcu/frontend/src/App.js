import React, { useState } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import Chatbot from './components/Chatbot';
import './components/Header.css';
import './components/Sidebar.css';
import './components/Chatbot.css';
import './App.css';

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  
  return (
    <div className="app-container">
      <Header />
      <div className="app-body">
        <Sidebar open={sidebarOpen} setOpen={setSidebarOpen} />
        <main className="main-content">
          <div className="chat-wrapper">
            <Chatbot />
          </div>
        </main>
      </div>
    </div>
  );
}

export default App;
