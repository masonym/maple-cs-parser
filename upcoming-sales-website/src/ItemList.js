import React, { useState, useEffect } from 'react';
import axios from 'axios';
import styles from './ItemList.module.css'

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
    console.log(items)
    useEffect(() => {
        axios.get('/api/items')
            .then(response => setItems(response.data))
            .catch(error => console.error(error));
    }, []);

    return (
        <div>
            <h1>Upcoming Sales</h1>
            <ul>
                {/* itemName = SN_ID, itemInfo = values  */}
                {Object.entries(items).map(([itemName, itemInfo]) => (
                    <li key={itemName.name}>
                        <div className={styles.itemFlexContainer}>
                            <img 
                                src={`./images/${itemInfo.itemID}.png`}
                                className={styles.itemImage}
                            />
                            <p>{itemInfo.name}</p>
                        </div>
                        <p>{convertNewlinesToBreaks(itemInfo.description)}</p>
                        <hr></hr>
                        <p>Duration: {itemInfo.period === '0' ? 'Permanent' : `${itemInfo.period} days`}</p>
                        <p>Price: {itemName.substring(0, 3) == '870' ? `${formatNumber(itemInfo.price)} Mesos ` : `${formatNumber(itemInfo.price)} NX`}</p>
                        <p>Start Date: {itemInfo.termStart}</p>
                        <p>End Date: {itemInfo.termEnd}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default ItemList;