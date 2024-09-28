import { FC } from 'react';
import styles from './Header.module.css';

const Header: FC = () => {
  return (
    <div className={styles.header}>
      <img src="/Logo_RUTUBE_dark_color.png" alt="Logo" width="150" />
    </div>
  );
};

export default Header;
