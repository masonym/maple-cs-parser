import React, { useState, useEffect } from 'react';
import axios from 'axios';
import styles from './ItemList.module.css';

const formatNumber = (number) => {
    return new Intl.NumberFormat('en-US').format(number);
};

// Function to convert text with '\n' into an array of <br> elements
const convertNewlinesToBreaks = (text) => {
    if (!text) return null; // Handle null or undefined descriptions gracefully

    return text.split('\n').map((line, index) => (
        <React.Fragment key={index}>
            {line}
            <br />
        </React.Fragment>
    ));
};

function ItemList() {
    const [items, setItems] = useState({});
    const [sortedKeys, setSortedKeys] = useState([]);
    const [sortKey, setSortKey] = useState('termStart');
    const [sortOrder, setSortOrder] = useState('asc');

    useEffect(() => {
        axios.get('/api/items')
            .then(response => {
                setItems(response.data);
                setSortedKeys(Object.keys(response.data));
            })
            .catch(error => console.error(error));
    }, []);

    // Function to sort the keys array based on item attributes
    const sortItems = () => {
        const newSortedKeys = [...sortedKeys].sort((a, b) => {
            let valA = items[a][sortKey];
            let valB = items[b][sortKey];

            // Convert date strings to Date objects for comparison if key is termStart or termEnd
            if (sortKey === 'termStart' || sortKey === 'termEnd') {
                valA = new Date(valA);
                valB = new Date(valB);
            }

            // Convert to numbers for comparison if key is 'price'
            if (sortKey === 'price') {
                valA = Number(valA);
                valB = Number(valB);
            }

            if (valA < valB) {
                return sortOrder === 'asc' ? -1 : 1;
            }
            if (valA > valB) {
                return sortOrder === 'asc' ? 1 : -1;
            }
            return 0;
        });

        // Update state with the new sorted keys
        setSortedKeys(newSortedKeys);
    };

    // Handle changes in the sorting attribute dropdown
    const handleSortKeyChange = (event) => {
        setSortKey(event.target.value);
        sortItems();
    };

    // Handle changes in the sorting order dropdown
    const handleSortOrderChange = (event) => {
        setSortOrder(event.target.value);
        sortItems();
    };

    // Trigger sorting when sortKey or sortOrder changes
    useEffect(() => {
        sortItems();
    }, [sortKey, sortOrder]);

    return (
        <div>
            <h1>Upcoming Sales</h1>
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
            </div>
            <ul className={styles.itemList}>
                {sortedKeys.map((key) => (
                    <li key={key} className={styles.item}>
                        <div className={styles.itemFlexContainer}>
                            <img 
                                src={`./images/${items[key].itemID}.png`}
                                className={styles.itemImage}
                                alt={items[key].name}
                            />
                            <p>{items[key].name}</p>
                        </div>
                        <p>{convertNewlinesToBreaks(items[key].description)}</p>
                        <hr />
                        <p>Duration: {items[key].period === '0' ? 'Permanent' : `${items[key].period} days`}</p>
                        <p>Price: {formatNumber(items[key].price)}{key.substring(0, 3) === '870' ? ' Mesos' : ' NX'}</p>
                        <p>Start Date: {items[key].termStart}</p>
                        <p>End Date: {items[key].termEnd}</p>
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