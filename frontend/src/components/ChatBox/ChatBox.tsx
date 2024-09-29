import { useState, FC } from 'react';
import styles from './ChatBox.module.css';
import axios from 'axios';
interface Message {
  text: string;
  sender: string;
}

interface ChatBoxProps {
  onBotReply: (message: Message) => void;
  onBotEdit: (message: string) => void;
}

const MiniChat: FC<ChatBoxProps> = ({ onBotReply, onBotEdit }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState<string>('');
  const [botMessage, setBotMessage] = useState<Message | null>(null);
  const [isChatOpen, setChatOpen] = useState<boolean>(false);

  const toggleChat = () => {
    setChatOpen((prevState) => !prevState);
  };

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage: Message = { text: input, sender: 'user' };
    setMessages([...messages, userMessage]);
    setInput('');

    try {
      const response = await axios.post('http://87.242.119.60:85/predict', {
        question: input,
      });

      const newBotMessage: Message = {
        text: response.data.answer,
        sender: 'bot',
      };
      setBotMessage(newBotMessage);

      setMessages((prevMessages) => [...prevMessages, newBotMessage]);
    } catch (error) {
      if (error instanceof Error) {
        console.error('Error sending message:', error.message);
      } else {
        console.error('Unexpected error:', error);
      }
    }
  };

  const sendMessageFromUser = () => {
    if (botMessage) {
      onBotReply(botMessage);
    } else {
      onBotReply({ text: '', sender: 'bot' });
    }
  };

  const editMessageFromUser = () => {
    if (botMessage) {
      onBotEdit(botMessage.text);
    } else {
      onBotEdit('');
    }
  };

  return (
    <div>
      <div className={styles.chatButtonContainer}>
        <button onClick={toggleChat} className={styles.chatButton}>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className={styles.addIcon}
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M12 6v6m0 0v6m0-6h6m-6 0H6"
            />
          </svg>
          Чат с помощником
        </button>
      </div>

      {isChatOpen && (
        <div className={styles.chatContainer}>
          <div className={styles.chatBox}>
            <div className={styles.header}>
              <p className="text-lg font-semibold">Интеллектуальный помощник</p>
              <button onClick={toggleChat} className={styles.closeButton}>
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className={styles.closeIcon}
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            </div>
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
              <div className={styles.buttonContainer}>
                <button onClick={sendMessageFromUser}>
                  Отправить пользователю
                </button>
                <button onClick={editMessageFromUser}>Изменить</button>
              </div>
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Type your message..."
                onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MiniChat;
