import React, { useState, useEffect } from 'react';
import axios from 'axios';
import styles from './ItemList.module.css';

const formatNumber = (number) => {
    return new Intl.NumberFormat('en-US').format(number);
};

const convertNewlinesToBreaks = (text) => {
    if (!text) return null;

    return text.split('\n').map((line, index) => (
        <React.Fragment key={index}>
            {line}
            <br />
        </React.Fragment>
    ));
};

const renderPackageContents = (contents) => {
    if (!contents) return null;

    return (
        <ul className={styles.packageContents}>
            {Object.entries(contents).map(([packageKey, packageItems]) => (
                <li key={packageKey}>
                    <strong>Includes:</strong>
                    <ul className={styles.packageItems}>
                        {Object.entries(packageItems).map(([itemIndex, itemDetails]) => {
                            const countText = itemDetails.count > 1 ? ` (x${itemDetails.count})` : '';
                            return (
                                <li key={itemIndex} className={styles.packageItem}>
                                    <div className={styles.packageItemFlexContainer}>
                                        <img 
                                            src={`./images/${itemDetails.itemID}.png`} 
                                            alt={itemDetails.name} 
                                            className={styles.packageItemImage} 
                                            onError={(e) => { e.target.style.display = 'none'; }} // hide the image if it doesn't exist
                                        />
                                        <div>
                                            <p>{itemDetails.name}{countText}</p>
                                            {itemDetails.description && <p><i>{convertNewlinesToBreaks(itemDetails.description)}</i></p>}
                                        </div>
                                    </div>
                                </li>
                            );
                        })}
                    </ul>
                </li>
            ))}
        </ul>
    );
};

function ItemList() {
    const [items, setItems] = useState({});
    const [sortedKeys, setSortedKeys] = useState([]);
    const [sortKey, setSortKey] = useState('termStart');
    const [sortOrder, setSortOrder] = useState('asc');
    const [hidePastItems, setHidePastItems] = useState(false);

    useEffect(() => {
        axios.get('https://my-worker.nosamleitch.workers.dev/api/items')
            .then(response => {
                const allItems = response.data;
                setItems(allItems);

                const sortedAndFilteredKeys = Object.keys(allItems)
                    .sort((a, b) => {
                        let valA = allItems[a][sortKey];
                        let valB = allItems[b][sortKey];

                        if (sortKey === 'termStart' || sortKey === 'termEnd') {
                            valA = new Date(valA);
                            valB = new Date(valB);
                        }

                        if (sortKey === 'price') {
                            valA = Number(valA);
                            valB = Number(valB);
                        }

                        if (valA < valB) return sortOrder === 'asc' ? -1 : 1;
                        if (valA > valB) return sortOrder === 'asc' ? 1 : -1;
                        return 0;
                    })
                    .filter(key => new Date(allItems[key].termStart) > new Date());

                setSortedKeys(sortedAndFilteredKeys);
            })
            .catch(error => console.error(error));
    }, [sortKey, sortOrder]); // Include sortKey and sortOrder in the dependency array

    useEffect(() => {
        const sortItems = () => {
            const newSortedKeys = [...Object.keys(items)].sort((a, b) => {
                let valA = items[a][sortKey];
                let valB = items[b][sortKey];

                if (sortKey === 'termStart' || sortKey === 'termEnd') {
                    valA = new Date(valA);
                    valB = new Date(valB);
                }

                if (sortKey === 'price') {
                    valA = Number(valA);
                    valB = Number(valB);
                }

                if (valA < valB) return sortOrder === 'asc' ? -1 : 1;
                if (valA > valB) return sortOrder === 'asc' ? 1 : -1;
                return 0;
            });

            const filteredKeys = hidePastItems ? newSortedKeys : newSortedKeys.filter(key => new Date(items[key].termStart) > new Date());

            setSortedKeys(filteredKeys);
        };

        sortItems();
    }, [sortKey, sortOrder, items, hidePastItems]); // Include all dependencies in the dependency array

    const handleSortKeyChange = (event) => {
        setSortKey(event.target.value);
    };

    const handleSortOrderChange = (event) => {
        setSortOrder(event.target.value);
    };

    const toggleHidePastItems = (event) => {
        setHidePastItems(event.target.checked);
    };

    return (
        <div>
            <h1>MapleStory Upcoming Cash Shop Sales</h1>
            <div className={styles.sortControls}>
                <label htmlFor="sortKey">Sort by: </label>
                <select id="sortKey" value={sortKey} onChange={handleSortKeyChange} className={styles.dropdown}>
                    <option value="name">Name</option>
                    <option value="price">Price</option>
                    <option value="termStart">Start Date</option>
                    <option value="termEnd">End Date</option>
                </select>
                <label htmlFor="sortOrder">Order: </label>
                <select id="sortOrder" value={sortOrder} onChange={handleSortOrderChange} className={styles.dropdown}>
                    <option value="asc">Ascending</option>
                    <option value="desc">Descending</option>
                </select>
                <label className={styles.checkboxLabel}>
                    <input 
                        type="checkbox" 
                        checked={hidePastItems} 
                        onChange={toggleHidePastItems} 
                        className={styles.checkboxInput}
                    />
                    Show Past Items
                </label>
            </div>
            <ul className={styles.itemList}>
                {sortedKeys.map((key) => (
                    <li key={key} className={styles.item}>
                        <div className={styles.itemFlexContainer}>
                            <img 
                                src={`./images/${items[key].itemID}.png`}
                                className={styles.itemImage}
                                alt={items[key].name}
                                onError={(e) => { e.target.style.display = 'none'; }}
                            />
                            <p>{items[key].name}</p>
                        </div>
                        <p>{convertNewlinesToBreaks(items[key].description)}</p>
                        <hr />
                        <p>Duration: {items[key].period === '0' ? 'Permanent' : `${items[key].period} days`}</p>
                        <p>Price: {formatNumber(items[key].price)}{key.substring(0, 3) === '870' ? ' Mesos' : ' NX'}</p>
                        <p>Start Date: {items[key].termStart}</p>
                        <p>End Date: {items[key].termEnd}</p>
                        {renderPackageContents(items[key].packageContents)}
                        {items[key].gameWorld.split('/').map((gameWorldId) => (
                            <img className={styles.gameWorld}
                                key={gameWorldId} 
                                src={`./gameWorlds/${gameWorldId}.png`} 
                                alt={`Game World ${gameWorldId}`} 
                                onError={(e) => { e.target.style.display = 'none'; }} // hide the image if it doesn't exist
                            />
                        ))}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default ItemList;