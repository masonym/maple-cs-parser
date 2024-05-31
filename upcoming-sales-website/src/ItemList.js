import React, { useState, useEffect } from 'react';
import axios from 'axios';
import styles from './assets/ItemList.module.css';
import { Helmet } from 'react-helmet';
import SortControls from './components/SortControls';
import FilterControls from './components/FilterControls';
import ItemCard from './components/ItemCard';
import Footer from './components/Footer';
import { formatDate } from './utils';

const intWorlds = [0, 1, 17, 18, 30, 48, 49];
const heroWorlds = [45, 46, 70];

function ItemList() {
    const [items, setItems] = useState({});
    const [categorizedItems, setCategorizedItems] = useState({});
    const [sortKey, setSortKey] = useState('termStart');
    const [sortOrder, setSortOrder] = useState('asc');
    const [hidePastItems, setHidePastItems] = useState(false);
    const [searchTerm, setSearchTerm] = useState('');
    const [worldFilter, setWorldFilter] = useState('');
    const [noItems, setNoItems] = useState(false);

    const handleSortKeyChange = (event) => setSortKey(event.target.value);
    const handleSortOrderChange = (event) => setSortOrder(event.target.value);
    const toggleHidePastItems = (event) => setHidePastItems(event.target.checked);
    const handleSearchTermChange = (event) => setSearchTerm(event.target.value.toLowerCase());
    const handleWorldFilterChange = (filter) => setWorldFilter(filter);

    const categorizeItems = (items) => {
        const categorized = {};

        Object.keys(items).forEach((key) => {
            const startDate = new Date(items[key].termStart);
            const dateKey = `${startDate.getFullYear()}-${(startDate.getMonth() + 1).toString().padStart(2, '0')}-${startDate.getDate().toString().padStart(2, '0')}`;

            if (!categorized[dateKey]) {
                categorized[dateKey] = [];
            }
            categorized[dateKey].push({ key, item: items[key] });
        });

        return categorized;
    };

    useEffect(() => {
        axios.get('https://masonym.dev/salesAPI/v1')
            .then(response => {
                const allItems = response.data;
                setItems(allItems);
                const categorized = categorizeItems(allItems);
                setCategorizedItems(categorized);
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
                        return worldIds.some(id => intWorlds.includes(id));
                    }
                    if (worldFilter === 'heroWorlds') {
                        return worldIds.some(id => heroWorlds.includes(id));
                    }
                    return true;
                });

            setNoItems(filteredKeys.length === 0);

            const sortedAndFilteredItems = {};
            filteredKeys.forEach(key => {
                const startDate = new Date(items[key].termStart);
                const dateKey = `${startDate.getFullYear()}-${(startDate.getMonth() + 1).toString().padStart(2, '0')}-${startDate.getDate().toString().padStart(2, '0')}`;
                if (!sortedAndFilteredItems[dateKey]) {
                    sortedAndFilteredItems[dateKey] = [];
                }
                sortedAndFilteredItems[dateKey].push({ key, item: items[key] });
            });

            setCategorizedItems(sortedAndFilteredItems);
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
            <h4> Last Updated for v.250.3.0 (May 30, 2024) </h4>
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
            {noItems ? (
                <p className={styles.noItemsMessage}>No items found</p>
            ) : (
                <div>
                    {Object.keys(categorizedItems).map((dateKey) => (
                        <div key={dateKey}>
                            <h2 className={styles.categoryHeader}>{formatDate(dateKey)}</h2>
                            <ul className={styles.itemList}>
                                {categorizedItems[dateKey].map(({ key, item }) => (
                                    <ItemCard key={key} item={item} />
                                ))}
                            </ul>
                        </div>
                    ))}
                </div>
            )}
            <Footer />
        </div>
    );
}

export default ItemList;
