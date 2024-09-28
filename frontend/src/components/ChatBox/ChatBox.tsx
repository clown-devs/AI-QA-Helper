import React, { useState } from 'react';
import styles from './ChatBox.module.css';

interface Message {
  text: string;
  sender: 'user' | 'bot';
}

const MiniChat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState<string>('');

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage: Message = { text: input, sender: 'user' };
    setMessages([...messages, userMessage]);
    setInput('');

    try {
      const response = await fetch('https://your-api-endpoint.com/chatbot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: input }),
      });
      const data = await response.json();

      const botMessage: Message = { text: data.response, sender: 'bot' };
      setMessages((prevMessages) => [...prevMessages, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  return (
    <div className={styles.miniChatbox}>
      <div className={styles.header}>Интеллектуальный помощник</div>
      <div className={styles.messagesContainer}>
        {messages
          .slice()
          .reverse()
          .map((message, index) => (
            <div
              key={index}
              className={`${styles.message} ${
                message.sender === 'user' ? styles.user : styles.bot
              }`}
            >
              {message.text}
            </div>
          ))}
      </div>
      <div className={styles.inputContainer}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
};

export default MiniChat;
