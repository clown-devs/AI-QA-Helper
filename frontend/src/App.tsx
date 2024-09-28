import React from 'react';
import Header from './components/Header/Header';
import Chat from './components/Chat/Chat';
import ChatBox from './components/ChatBox/ChatBox';
import styles from './App.module.css';

// interface Message {
//   text: string;
//   sender: string;
// }

const App: React.FC = () => {
  // const [messages, setMessages] = useState<Message[]>([]);

  // const addMessage = (message: Message) => {
  //   setMessages((prevMessages) => [...prevMessages, message]);
  // };

  return (
    <div className={styles['app-container']}>
      <Header />
      <div className={styles.container}>
        <Chat />
        <ChatBox />
      </div>
    </div>
  );
};

export default App;
