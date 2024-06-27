import React from 'react';
import styles from '../assets/AdvancedItemCardHover.module.css';
import { formatNumber, convertNewlinesToBreaks, formatSaleTimesDate, calculateDateDifference, magicText } from '../utils';
import AdvancedPackageContents from './AdvancedPackageContents';

const AdvancedItemCardHover = ({ item, position, isTouchDevice, hoverCardRef, onClose }) => {
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
                <img
                    src={`./images/${item.itemID}.png`}
                    className={styles.itemImage}
                    alt={item.name}
                    onError={(e) => { e.target.style.display = 'none'; }}
                />
                <p>{convertNewlinesToBreaks(item.description)}</p>
            </div>
            <AdvancedPackageContents contents={item.packageContents} />
            <hr />
            <p>Price: {formatNumber(item.price)}{item.itemID.toString().startsWith('870') ? ' Mesos' : ' NX'} {item.discount === 1 ? `(was ${formatNumber(item.originalPrice)}${item.itemID.toString().startsWith('870') ? ' Mesos' : ' NX'})` : ''}</p>
        </div>
    );
};

export default AdvancedItemCardHover;