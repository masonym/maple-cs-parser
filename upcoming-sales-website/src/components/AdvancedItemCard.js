import React from 'react';
import styles from '../assets/AdvancedItemCard.module.css';
import { formatNumber, convertNewlinesToBreaks, formatSaleTimesDate, calculateDateDifference } from '../utils';
import PackageContents from './PackageContents';
import background from '../assets/productBg.png'

const AdvancedItemCard = ({ item }) => {
    return (
        <li key={item.itemID} className={styles.item}>
            <div className={styles.itemFlexContainer} style={{ backgroundImage: `url(${background})` }}>
                <img
                    src={`./images/${item.itemID}.png`}
                    className={styles.itemImage}
                    alt={item.name}
                    onError={(e) => { e.target.style.display = 'none'; }}
                />
                <div className={styles.itemDetails}>
                    <p className={styles.itemName}>{item.name}</p>
                    <p className={styles.itemPrice}>{formatNumber(item.price)} NX</p>
                </div>
            </div>
        </li>
    );
};

export default AdvancedItemCard;
