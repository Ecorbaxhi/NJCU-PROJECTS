import React, { useState, useRef, useEffect } from 'react';
import './Chatbot.css';

function Chatbot() {
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Welcome to NJCU! How can I help you today?' }
  ]);
  const [input, setInput] = useState('');
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = () => {
    if (!input.trim()) return;
    setMessages([...messages, { sender: 'user', text: input }]);
    setInput('');
    // Simulate bot response
    setTimeout(() => {
      setMessages(msgs => [...msgs, { sender: 'bot', text: 'Thank you for your question! (This is a demo response.)' }]);
    }, 800);
  };

  return (
    <div className="chatbot-container">
      <div className="chatbot-header">NJCU Student Chatbot</div>
      <div className="chatbot-messages">
        {messages.map((msg, idx) => (
          <div key={idx} className={`chat-message ${msg.sender}`}>{msg.text}</div>
        ))}
        <div ref={chatEndRef} />
      </div>
      <div className="chatbot-input-area">
        <input
          type="text"
          className="chatbot-input"
          placeholder="Type your question..."
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && sendMessage()}
        />
        <button className="chatbot-send-btn" onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}

export default Chatbot;