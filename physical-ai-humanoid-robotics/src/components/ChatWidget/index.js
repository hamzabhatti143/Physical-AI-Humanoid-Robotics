import React, { useState } from 'react';
import ChatInterface from './ChatInterface';
import styles from './styles.module.css';

export default function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className={styles.chatWidgetContainer}>
      {isOpen && <ChatInterface onClose={toggleChat} />}
      
      <button 
        className={styles.chatButton}
        onClick={toggleChat}
        aria-label="Toggle chat"
      >
        {isOpen ? '✕' : '💬'}
      </button>
    </div>
  );
}