import React, { useState } from 'react';
import styles from '../assets/AdvancedItemCard.module.css';
import { formatNumber, convertNewlinesToBreaks, formatSaleTimesDate, calculateDateDifference } from '../utils';
import background from '../assets/productBg.png'
import AdvancedItemCardHover from './AdvancedItemCardHover';

const AdvancedItemCard = ({ item }) => {
    const [isHovering, setIsHovering] = useState(false);
    const [hoverPosition, setHoverPosition] = useState({ x: 0, y: 0 });
  
    const handleMouseEnter = () => {
      setIsHovering(true);
    };
  
    const handleMouseLeave = () => {
      setIsHovering(false);
    };
  
    const handleMouseMove = (e) => {
      setHoverPosition({ x: e.clientX + 10, y: e.clientY + 10 });
    };
  
    return (
      <li
        className={styles.item}
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
        onMouseMove={handleMouseMove}
      >
        <li key={item.itemID} className={styles.item}>
            
            <div className={styles.itemFlexContainer} style={{ backgroundImage: `url(${background})` }}>
                <img
                    src={`./images/${item.itemID}.png`}
                    className={styles.itemImage}
                    alt={item.name}
                    onError={(e) => { e.target.style.display = 'none'; }}
                />
                <div className={styles.itemDetails}>
                    <p className={styles.itemName}>{item.name}{item.count > 1 ? ` (x${item.count})` : ''}</p>
                    <p className={styles.itemPrice}>{formatNumber(item.price)} NX</p>
                </div>
            </div>
        </li>
        {isHovering && (
        <AdvancedItemCardHover item={item} position={hoverPosition} />
      )}
    </li>
  );
};

export default AdvancedItemCard;