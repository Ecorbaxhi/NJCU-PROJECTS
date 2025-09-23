import React, { useState, useRef, useEffect } from 'react';
import './Chatbot.css';

function Chatbot() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const chatEndRef = useRef(null);
  const inputRef = useRef(null);

  const suggestedQuestions = [
    "What are NJCU's admission requirements?",
    "How do I register for classes?",
    "What dining options are available?",
    "Where is the library located?"
  ];

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = (messageText = input) => {
    if (!messageText.trim()) return;
    
    const userMessage = { sender: 'user', text: messageText.trim() };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsTyping(true);
    setIsLoading(true);
    
    // Simulate bot response with realistic delay
    setTimeout(() => {
      setIsTyping(false);
      const botResponse = {
        sender: 'bot',
        text: `Thank you for asking about "${messageText.trim()}". I'm currently in demo mode, but I'd be happy to help you with NJCU-related questions. Please contact our student services for detailed information.`
      };
      setMessages(prev => [...prev, botResponse]);
      setIsLoading(false);
    }, 1200 + Math.random() * 800);
  };

  const handleSuggestedQuestion = (question) => {
    sendMessage(question);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="chatbot-container">
      <div className="chatbot-messages">
        {messages.length === 0 ? (
          <div className="empty-state">
            <div className="empty-state-icon">🎓</div>
            <h3>Welcome to NJCU!</h3>
            <p>I'm your AI assistant here to help with questions about New Jersey City University. Ask me anything!</p>
            <div className="suggested-questions">
              {suggestedQuestions.map((question, idx) => (
                <button
                  key={idx}
                  className="suggested-question"
                  onClick={() => handleSuggestedQuestion(question)}
                >
                  {question}
                </button>
              ))}
            </div>
          </div>
        ) : (
          <>
            {messages.map((msg, idx) => (
              <div key={idx} className={`chat-message ${msg.sender}`}>
                {msg.text}
              </div>
            ))}
            {isTyping && (
              <div className="typing-indicator">
                <span>NJCU Assistant is typing</span>
                <div className="typing-dots">
                  <div className="typing-dot"></div>
                  <div className="typing-dot"></div>
                  <div className="typing-dot"></div>
                </div>
              </div>
            )}
          </>
        )}
        <div ref={chatEndRef} />
      </div>
      
      <div className="chatbot-input-area">
        <div className="input-wrapper">
          <textarea
            ref={inputRef}
            className="chatbot-input"
            placeholder="Type your question about NJCU..."
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            rows={1}
            disabled={isLoading}
          />
        </div>
        <div className="input-actions">
          <button className="attachment-btn" title="Attach file">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M21.44 11.05l-9.19 9.19a6 6 0 01-8.49-8.49l9.19-9.19a4 4 0 015.66 5.66L9.64 16.2a2 2 0 01-2.83-2.83l8.49-8.49" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </button>
          <button 
            className="chatbot-send-btn" 
            onClick={() => sendMessage()}
            disabled={!input.trim() || isLoading}
          >
            {isLoading ? (
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2" strokeDasharray="31.416" strokeDashoffset="31.416">
                  <animate attributeName="stroke-dasharray" dur="2s" values="0 31.416;15.708 15.708;0 31.416;0 31.416" repeatCount="indefinite"/>
                  <animate attributeName="stroke-dashoffset" dur="2s" values="0;-15.708;-31.416;-31.416" repeatCount="indefinite"/>
                </circle>
              </svg>
            ) : (
              <>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M22 2L11 13" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  <path d="M22 2L15 22L11 13L2 9L22 2Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
                Send
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}

export default Chatbot;