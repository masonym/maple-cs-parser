import React from 'react';
import styles from '../assets/AdvancedItemCardHover.module.css';
import { formatPriceDisplay, convertNewlinesToBreaks, formatSaleTimesDate, calculateDateDifference, magicText } from '../utils';
import AdvancedPackageContents from './AdvancedPackageContents';
import itemBase from '../assets/itemBase.png'

const AdvancedItemCardHover = ({ itemKey, item, position, isTouchDevice, hoverCardRef, onClose }) => {
    const hoverCardStyle = isTouchDevice ? styles.mobileHoverCard : styles.desktopHoverCard;
    const hoverCardPosition = isTouchDevice ? {} : { left: `${position.x}px`, top: `${position.y}px` };

    return (
        <div ref={hoverCardRef} className={`${styles.hoverCard} ${hoverCardStyle}`} style={hoverCardPosition}>
            {isTouchDevice && (
                <button className={styles.closeButton} onClick={(e) => {
                    e.stopPropagation();
                    onClose();
                }}>
                    &times;
                </button>
            )}
            <p>{item.name}{item.count > 1 ? ` (x${item.count})` : ''}</p>
            <div className={styles.saleTimes}>
                <p>{formatSaleTimesDate(item.termStart)} ~ {formatSaleTimesDate(item.termEnd)} UTC</p>
                <p>({calculateDateDifference(item.termStart, item.termEnd)})</p>
            </div>
            <p>{magicText(item.itemID)}Duration: {item.period === '0' ? 'Permanent' : `${item.period} days`}</p>
            <div className={styles.itemFlexContainer}>
                <div className={styles.itemImageContainer}>
                    <img
                        src={`./images/${item.itemID}.png`}
                        className={styles.itemImage}
                        alt={item.name}
                        onError={(e) => { e.target.style.display = 'none'; }}
                    />
                    <img
                        src={itemBase}
                        className={styles.itemImageBase}
                    />
                </div>
                <p>{convertNewlinesToBreaks(item.description)}</p>
            </div>
            <AdvancedPackageContents contents={item.packageContents} />
            <hr className={styles.hr} />
            <p className={styles.itemPrice}>
                {formatPriceDisplay(item.originalPrice, item.price, itemKey, item.discount)}
            </p>
        </div>
    );
};

export default AdvancedItemCardHover;