import React, { useState, useRef, useEffect } from 'react';
import styles from './styles.module.css';

export default function ChatInterface({ onClose }) {
  const [messages, setMessages] = useState([
    { type: 'bot', text: 'Hi! Ask me anything about Physical AI & Humanoid Robotics!' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = input.trim();
    setInput('');
    setMessages(prev => [...prev, { type: 'user', text: userMessage }]);
    setLoading(true);

    try {
      const backendUrl =  'https://hamzabhatti-chatbot.hf.space/';
      console.log('Sending request to:', `${backendUrl}/api/chat`);
      
      const response = await fetch(`${backendUrl}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: userMessage,
          user_id: 1
        }),
      });

      console.log('Response status:', response.status);
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error('Response error:', errorText);
        throw new Error(`HTTP ${response.status}: ${errorText}`);
      }

      const data = await response.json();
      console.log('Success:', data);
      
      setMessages(prev => [...prev, { 
        type: 'bot', 
        text: data.answer,
        sources: data.sources 
      }]);
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, { 
        type: 'bot', 
        text: `❌ Error: ${error.message}. Make sure server is running on http://localhost:8000`,
        isError: true
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.chatInterface}>
      <div className={styles.chatHeader}>
        <h3>AI Assistant</h3>
        <button onClick={onClose} className={styles.closeButton}>✕</button>
      </div>

      <div className={styles.messagesContainer}>
        {messages.map((msg, idx) => (
          <div key={idx} className={`${styles.message} ${styles[msg.type]}`}>
            <div className={styles.messageText}>
              {msg.text}
              {msg.sources && msg.sources.length > 0 && (
                <div className={styles.sources}>
                  <small>📚 Sources: {msg.sources.join(', ')}</small>
                </div>
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div className={`${styles.message} ${styles.bot}`}>
            <div className={styles.messageText}>
              <span className={styles.typingIndicator}>●●●</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className={styles.inputForm}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question..."
          className={styles.input}
          disabled={loading}
        />
        <button 
          type="submit" 
          className={styles.sendButton}
          disabled={loading || !input.trim()}
        >
          Send
        </button>
      </form>
    </div>
  );
}
