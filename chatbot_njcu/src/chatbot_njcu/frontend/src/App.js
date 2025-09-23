import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import Chatbot from './components/Chatbot';
import './components/Sidebar.css';
import './components/Chatbot.css';

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  return (
    <div style={{ display: 'flex', height: '100vh', background: '#f5f5f5' }}>
      <Sidebar open={sidebarOpen} setOpen={setSidebarOpen} />
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', background: '#f5f5f5' }}>
        <Chatbot />
      </div>
    </div>
  );
}

export default App;
