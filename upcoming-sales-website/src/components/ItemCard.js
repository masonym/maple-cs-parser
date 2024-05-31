import React from 'react';
import styles from '../assets/ItemList.module.css';
import { formatNumber, convertNewlinesToBreaks } from '../utils';
import PackageContents from './PackageContents';

const ItemCard = ({ item }) => {
    return (
        <li key={item.itemID} className={styles.item}>
            <div className={styles.itemContent}>
                <div className={styles.itemFlexContainer}>
                    <img
                        src={`./images/${item.itemID}.png`}
                        className={styles.itemImage}
                        alt={item.name}
                        onError={(e) => { e.target.style.display = 'none'; }}
                    />
                    <p>{item.name}{item.count > 1 ? ` (x${item.count})` : ''}</p>
                </div>
                <p>{convertNewlinesToBreaks(item.description)}</p>
                <hr />
                <p>Duration: {item.period === '0' ? 'Permanent' : `${item.period} days`}</p>
                <p>Price: {formatNumber(item.price)}{item.itemID.toString().startsWith('870') ? ' Mesos' : ' NX'} {item.discount == 1 ? `(was ${formatNumber(item.originalPrice)}${item.itemID.toString().startsWith('870') ? ' Mesos' : ' NX'})` : ''}</p>
                <p>Start Date: {item.termStart}</p>
                <p>End Date: {item.termEnd}</p>
                <PackageContents contents={item.packageContents} />
            </div>
            <div className={styles.gameWorldContainer}>
                {item.gameWorld.split('/').map((gameWorldId) => (
                    <img className={styles.gameWorld}
                        key={gameWorldId}
                        src={`./gameWorlds/${gameWorldId}.png`}
                        alt={`Game World ${gameWorldId}`}
                        onError={(e) => { e.target.style.display = 'none'; }} // hide the image if it doesn't exist
                    />
                ))}
            </div>
        </li>
    );
};

export default ItemCard;
