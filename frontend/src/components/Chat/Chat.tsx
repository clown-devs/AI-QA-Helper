import React, { useState } from 'react';
import styles from './Chat.module.css';

const Chat: React.FC = () => {
  const [messages, setMessages] = useState<string[]>([]);
  const [input, setInput] = useState<string>('');

  const handleSend = () => {
    if (input.trim()) {
      setMessages([...messages, input]);
      setInput('');
    }
  };

  return (
    <div className={styles.chatContainer}>
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
          placeholder="Введите запрос..."
          className={styles.input}
        />
        <button onClick={handleSend} className={styles.sendButton}>
          Отправить
        </button>
      </div>
    </div>
  );
};

export default Chat;

// import React, { useState } from 'react';
// import styles from './Chat.module.css';

// type Message = {
//   text: string;
//   sender: 'user' | 'system'; // Указываем тип отправителя
// };

// const Chat: React.FC = () => {
//   const [messages, setMessages] = useState<Message[]>([]);
//   const [input, setInput] = useState<string>('');

//   const handleSend = () => {
//     if (input.trim()) {
//       const userMessage: Message = { text: input, sender: 'user' };
//       setMessages((prevMessages) => [...prevMessages, userMessage]);
//       setInput('');

//       // Имитация ответа от системы через 1 секунду
//       setTimeout(() => {
//         const systemMessage: Message = {
//           text: `Ответ на: "${input}"`,
//           sender: 'system',
//         };
//         setMessages((prevMessages) => [...prevMessages, systemMessage]);
//       }, 1000);
//     }
//   };

//   return (
//     <div className={styles.chatContainer}>
//       <div className={styles.messages}>
//         {messages.map((msg, index) => (
//           <div
//             key={index}
//             className={`${styles.message} ${
//               msg.sender === 'user' ? styles.userMessage : styles.systemMessage
//             }`}
//           >
//             {msg.text}
//           </div>
//         ))}
//       </div>
//       <div className={styles.inputContainer}>
//         <input
//           type="text"
//           value={input}
//           onChange={(e) => setInput(e.target.value)}
//           placeholder="Введите запрос..."
//           className={styles.input}
//         />
//         <button onClick={handleSend} className={styles.sendButton}>
//           Отправить
//         </button>
//       </div>
//     </div>
//   );
// };

// export default Chat;
