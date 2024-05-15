// ItemList.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import styles from './assets/ItemList.module.css';
import { Helmet } from 'react-helmet';
import SortControls from './components/SortControls';
import FilterControls from './components/FilterControls';
import ItemCard from './components/ItemCard';
import { formatNumber } from './utils';

const intWorlds = [0, 1, 17, 18, 30, 48, 49];
const heroWorlds = [45, 46, 70];

function ItemList() {
    const [items, setItems] = useState({});
    const [sortedKeys, setSortedKeys] = useState([]);
    const [sortKey, setSortKey] = useState('termStart');
    const [sortOrder, setSortOrder] = useState('asc');
    const [hidePastItems, setHidePastItems] = useState(false);
    const [searchTerm, setSearchTerm] = useState('');
    const [worldFilter, setWorldFilter] = useState('');

    const handleSortKeyChange = (event) => setSortKey(event.target.value);

    const handleSortOrderChange = (event) => setSortOrder(event.target.value);

    const toggleHidePastItems = (event) => setHidePastItems(event.target.checked);

    const handleSearchTermChange = (event) => setSearchTerm(event.target.value.toLowerCase());

    const handleWorldFilterChange = (filter) => setWorldFilter(filter);

    useEffect(() => {
        axios.get('https://masonym.dev/salesAPI/v1')
            .then(response => {
                const allItems = response.data;
                setItems(allItems);
            })
            .catch(error => console.error(error));
    }, []);

    useEffect(() => {
        const sortAndFilterItems = () => {
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

            const filteredKeys = newSortedKeys
                .filter(key => hidePastItems || new Date(items[key].termStart) > new Date())
                .filter(key => items[key].name.toLowerCase().includes(searchTerm))
                .filter(key => {
                    if (!worldFilter) return true;
                    const worldIds = items[key].gameWorld.split('/').map(Number);
                    if (worldFilter === 'intWorlds') {
                        return worldIds.every(id => intWorlds.includes(id));
                    }
                    if (worldFilter === 'heroWorlds') {
                        return worldIds.every(id => heroWorlds.includes(id));
                    }
                    return true;
                });

            setSortedKeys(filteredKeys);
        };

        sortAndFilterItems();
    }, [sortKey, sortOrder, items, hidePastItems, searchTerm, worldFilter]);

    return (
        <div>
            <Helmet>
                <title>Upcoming MapleStory Cash Shop Sales</title>
                <meta property="og:title" content="Upcoming MapleStory Cash Shop Sales" />
                <meta property="og:description" content="A tool to see upcoming items going on sale in MapleStory's cash shop!" />
                <meta property="twitter:title" content="Upcoming MapleStory Cash Shop Sales" />
                <meta property="twitter:description" content="A tool to see upcoming items going on sale in MapleStory's cash shop!" />
            </Helmet>
            <h1>MapleStory Upcoming Cash Shop Sales</h1>
            <SortControls
                sortKey={sortKey}
                sortOrder={sortOrder}
                onSortKeyChange={handleSortKeyChange}
                onSortOrderChange={handleSortOrderChange}
            />
            <FilterControls
                searchTerm={searchTerm}
                hidePastItems={hidePastItems}
                worldFilter={worldFilter}
                onSearchTermChange={handleSearchTermChange}
                onHidePastItemsChange={toggleHidePastItems}
                onWorldFilterChange={handleWorldFilterChange}
            />
            <ul className={styles.itemList}>
                {sortedKeys.map((key) => (
                    <ItemCard key={key} item={items[key]} />
                ))}
            </ul>
        </div>
    );
}

export default ItemList;