// ItemListMain.js
import React, { useState } from 'react';
import ItemList from './ItemList';
import AdvancedItemList from './AdvancedItemList';
import styles from './assets/ItemListMain.module.css';

function ItemListMain() {
  const [isAdvanced, setIsAdvanced] = useState(true);

  const toggleView = () => {
    setIsAdvanced(!isAdvanced);
  };

  return (
    <div className={styles.itemListMain}>
      <div className={styles.toggleContainer}>
        <div className={styles.toggleSwitch} onClick={toggleView}>
          <div className={`${styles.slider} ${isAdvanced ? styles.right : styles.left}`}>
            <span className={styles.icon}>{isAdvanced ? '🔍' : '👁️'}</span>
          </div>
        </div>
        <span className={`${styles.label} ${isAdvanced ? styles.advancedLabel : styles.simpleLabel}`}>
          {isAdvanced ? 'Advanced' : 'Simple'}
        </span>
      </div>
      <div className={styles.content}>
        {isAdvanced ? <AdvancedItemList /> : <ItemList />}
      </div>
    </div>
  );
}

export default ItemListMain;