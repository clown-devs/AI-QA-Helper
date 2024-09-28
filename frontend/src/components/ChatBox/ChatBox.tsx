import React, { useState } from 'react';
import styles from './ChatBox.module.css';
import axios from 'axios';
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
      const response = await axios.post('http://87.242.119.60:85/predict', {
        question: input,
      });
      console.log(response);

      const botMessage: Message = { text: response.data.answer, sender: 'bot' };
      setMessages((prevMessages) => [...prevMessages, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error.message || error);
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
        {/* <button onClick={sendMessage}>Отправить </button> */}
      </div>
    </div>
  );
};

export default MiniChat;
