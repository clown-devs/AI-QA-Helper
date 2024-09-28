import React, { useState } from 'react';
import styles from './ChatBox.module.css';

const ChatBox: React.FC = () => {
  const [input, setInput] = useState<string>('');
  const [messages, setMessages] = useState<string[]>([]);

  const handleSend = () => {
    if (input.trim()) {
      setMessages((prev) => [...prev, input]);
      setInput('');
    }
  };

  return (
    <div className={styles.chatBoxContainer}>
      <h3>Дополнительный чат</h3>
      <div className={styles.messages}>
        {messages.map((msg, index) => (
          <div key={index} className={styles.message}>
            {msg}
          </div>
        ))}
      </div>
      <div className={styles.inputContainer}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Введите сообщение для второго чата..."
          className={styles.input}
        />
        <button onClick={handleSend} className={styles.sendButton}>
          Отправить
        </button>
      </div>
    </div>
  );
};

export default ChatBox;
