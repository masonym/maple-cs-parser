import React from 'react';
import styles from '../assets/AdvancedItemCardHover.module.css';
import { formatNumber, convertNewlinesToBreaks, formatSaleTimesDate, calculateDateDifference } from '../utils';
import PackageContents from './PackageContents';

const AdvancedItemCardHover = ({ item, position }) => {
    return (
        <div className={styles.hoverCard} style={{ left: position.x, top: position.y }}>
            <div className={styles.saleTimes}>
                <p>{formatSaleTimesDate(item.termStart)} ~ {formatSaleTimesDate(item.termEnd)} UTC</p>
                <p>({calculateDateDifference(item.termStart, item.termEnd)})</p>
            </div>
            <div className={styles.itemFlexContainer}>
                <img
                    src={`./images/${item.itemID}.png`}
                    className={styles.itemImage}
                    alt={item.name}
                    onError={(e) => { e.target.style.display = 'none'; }}
                />
                <h3>{item.name}{item.count > 1 ? ` (x${item.count})` : ''}</h3>
            </div>
            <p>{convertNewlinesToBreaks(item.description)}</p>
            <hr />
            <p>Duration: {item.period === '0' ? 'Permanent' : `${item.period} days`}</p>
            <p>Price: {formatNumber(item.price)}{item.itemID.toString().startsWith('870') ? ' Mesos' : ' NX'} {item.discount == 1 ? `(was ${formatNumber(item.originalPrice)}${item.itemID.toString().startsWith('870') ? ' Mesos' : ' NX'})` : ''}</p>
            <PackageContents contents={item.packageContents} />
        </div>
    );
};

export default AdvancedItemCardHover;