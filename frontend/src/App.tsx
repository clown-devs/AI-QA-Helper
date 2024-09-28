import React from 'react';
import Header from './components/Header/Header';
import Chat from './components/Chat/Chat';
import styles from './App.module.css';

const App: React.FC = () => {
  return (
    <div className={styles['app-container']}>
      <Header />
      <div className={styles['chat-container']}>
        <Chat />
      </div>
      {/* <ChatBox /> */}
    </div>
  );
};

export default App;
