import { FC } from 'react';
import styles from './Chat.module.css';

interface Message {
  text: string;
  sender: string;
}

interface ChatProps {
  messages: Message[];
  addMessage: (message: Message) => void;
  inputValue: string;
  addInputValue: (inputValue: string) => void;
}

const Chat: FC<ChatProps> = ({
  messages,
  addMessage,
  inputValue,
  addInputValue,
}) => {
  const sendMessage = () => {
    if (inputValue.trim()) {
      const newMessage: Message = { text: inputValue, sender: 'user' };
      addMessage(newMessage);
      addInputValue('');
    }
  };

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter') {
      sendMessage();
    }
  };

  return (
    <div className={styles.chatContainer}>
      <div className={styles.header}>Чат с пользователем</div>
      <div className={styles.messages}>
        {messages
          .slice()
          .reverse()
          .map((message, index) => (
            <div className={styles.messageItem}>
              {/* <div className={styles.containerImg}>
                <img
                  src="/clown.png"
                  alt="Logo"
                  width="40"
                  height={40}
                  className={styles.logo}
                />
              </div> */}
              <div key={index} className={styles.message}>
                {message.text}
              </div>
            </div>
          ))}
      </div>
      <div className={styles.inputContainer}>
        <input
          type="text"
          value={inputValue}
          onChange={(e) => addInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type your message..."
          className={styles.input}
        />
        <button onClick={sendMessage} className={styles.sendButton}>
          Send
        </button>
      </div>
    </div>
  );
};

export default Chat;
