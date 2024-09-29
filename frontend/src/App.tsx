import { FC, useState } from 'react';
import Header from './components/Header/Header';
import Chat from './components/Chat/Chat';
import ChatBox from './components/ChatBox/ChatBox';
import styles from './App.module.css';

interface Message {
  text: string;
  sender: string;
}

const App: FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState<string>('');

  const addMessage = (message: Message) => {
    setMessages((prevMessages) => [...prevMessages, message]);
  };

  const addInputValue = (inputValue: string) => {
    setInputValue(inputValue);
  };

  return (
    <div className={styles['app-container']}>
      <Header />
      <div className={styles.container}>
        <Chat
          messages={messages}
          addMessage={addMessage}
          inputValue={inputValue}
          addInputValue={addInputValue}
        />
        <ChatBox onBotReply={addMessage} onBotEdit={addInputValue} />
      </div>
      {/* <div>
        <Header />
        <div className={styles.container}>
          <Chat
            messages={messages}
            addMessage={addMessage}
            inputValue={inputValue}
            addInputValue={addInputValue}
          />
          <ChatBox onBotReply={addMessage} onBotEdit={addInputValue} />
        </div>
      </div> */}
    </div>
  );
};

export default App;
