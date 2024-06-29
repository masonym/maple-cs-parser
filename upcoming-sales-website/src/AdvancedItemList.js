import React, { useState, useEffect } from 'react';
import axios from 'axios';
import advancedStyles from './assets/AdvancedItemList.module.css';
import { Helmet } from 'react-helmet';
import SortControls from './components/SortControls';
import FilterControls from './components/FilterControls';
import Footer from './components/Footer';
import { formatDate } from './utils';
import AdvancedItemCard from './components/AdvancedItemCard';
import background from './assets/backgrnd_cr.png';
import noItemsImage from './assets/noItem_mini.png';

const intWorlds = [0, 1, 17, 18, 30, 48, 49];
const heroWorlds = [45, 46, 70];

function AdvancedItemList() {
    const [items, setItems] = useState({});
    const [categorizedItems, setCategorizedItems] = useState({});
    const [sortKey, setSortKey] = useState('termStart');
    const [sortOrder, setSortOrder] = useState('asc');
    const [hidePastItems, setHidePastItems] = useState(false);
    const [showCurrentItems, setShowCurrentItems] = useState(false);
    const [searchTerm, setSearchTerm] = useState('');
    const [worldFilter, setWorldFilter] = useState('');
    const [noItems, setNoItems] = useState(false);
    const [openItemId, setOpenItemId] = useState(null);
    const [isTouchDevice, setIsTouchDevice] = useState(false);
    const [collapsedCategories, setCollapsedCategories] = useState({});

    const handleSortKeyChange = (event) => setSortKey(event.target.value);
    const handleSortOrderChange = (event) => setSortOrder(event.target.value);

    const toggleHidePastItems = (event) => {
        setHidePastItems(event.target.checked);
        if (event.target.checked) {
            setShowCurrentItems(false);
        }
    };

    const toggleShowCurrentItems = (event) => {
        setShowCurrentItems(event.target.checked);
        if (event.target.checked) {
            setHidePastItems(false);
        }
    };

    const toggleCategory = (dateKey) => {
        setCollapsedCategories(prev => ({
            ...prev,
            [dateKey]: !prev[dateKey]
        }));
    }

    const handleSearchTermChange = (event) => setSearchTerm(event.target.value.toLowerCase());
    const handleWorldFilterChange = (filter) => setWorldFilter(filter);

    const parseDate = (dateString) => {
        const [datePart, timePart] = dateString.split(' ');
        const [month, day, year] = datePart.split('-');
        const [hour, minute] = timePart.split(':');
        return new Date(Date.UTC(year, month - 1, day, hour, minute));
    };

    const categorizeItems = (items) => {
        const categorized = {};

        Object.keys(items).forEach((key) => {
            const startDate = parseDate(items[key].termStart);
            const dateKey = `${startDate.getUTCFullYear()}-${(startDate.getUTCMonth() + 1).toString().padStart(2, '0')}-${startDate.getUTCDate().toString().padStart(2, '0')}`;

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
            const now = new Date().getTime();

            const newSortedKeys = [...Object.keys(items)].sort((a, b) => {
                let valA = items[a][sortKey];
                let valB = items[b][sortKey];

                if (sortKey === 'termStart' || sortKey === 'termEnd') {
                    valA = parseDate(valA).getTime();
                    valB = parseDate(valB).getTime();
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
                .filter(key => {
                    const termStart = parseDate(items[key].termStart).getTime();
                    const termEnd = parseDate(items[key].termEnd).getTime();

                    // Filter logic based on the checkboxes
                    if (hidePastItems && termEnd >= now) return false; // Hide past items if checked
                    if (showCurrentItems && !(termStart <= now && termEnd >= now)) return false; // Show only current items if checked

                    // Show only upcoming items by default
                    if (!hidePastItems && !showCurrentItems && termStart <= now) return false;

                    return true;
                })
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
                const startDate = parseDate(items[key].termStart);
                const dateKey = `${startDate.getUTCFullYear()}-${(startDate.getUTCMonth() + 1).toString().padStart(2, '0')}-${startDate.getUTCDate().toString().padStart(2, '0')}`;
                if (!sortedAndFilteredItems[dateKey]) {
                    sortedAndFilteredItems[dateKey] = [];
                }
                sortedAndFilteredItems[dateKey].push({ key, item: items[key] });
            });

            setCategorizedItems(sortedAndFilteredItems);
        };

        sortAndFilterItems();
    }, [sortKey, sortOrder, items, hidePastItems, showCurrentItems, searchTerm, worldFilter]);

    useEffect(() => {
        setIsTouchDevice('ontouchstart' in window || navigator.maxTouchPoints > 0);
    }, []);

    const handleItemClick = (itemId) => {
        if (isTouchDevice) {
            setOpenItemId(prevId => prevId === itemId ? null : itemId);
        }
    };

    return (
        <div className={advancedStyles.mainContent} style={{
            backgroundImage: `url(${background})`,
            backgroundAttachment: 'fixed',
        }}>
            <Helmet>
                <title>Upcoming MapleStory Cash Shop Sales</title>
                <meta property="og:title" content="Upcoming MapleStory Cash Shop Sales" />
                <meta property="og:description" content="A tool to see upcoming items going on sale in MapleStory's cash shop!" />
                <meta property="twitter:title" content="Upcoming MapleStory Cash Shop Sales" />
                <meta property="twitter:description" content="A tool to see upcoming items going on sale in MapleStory's cash shop!" />
            </Helmet>
            <h1 className={advancedStyles.h1}>MapleStory Upcoming Cash Shop Sales</h1>
            <h4 className={advancedStyles.h4}> Last Updated for v.251 (June 12th, 2024) </h4>
            <SortControls
                sortKey={sortKey}
                sortOrder={sortOrder}
                onSortKeyChange={handleSortKeyChange}
                onSortOrderChange={handleSortOrderChange}
                className={advancedStyles}
            />
            <FilterControls
                searchTerm={searchTerm}
                hidePastItems={hidePastItems}
                showCurrentItems={showCurrentItems}
                worldFilter={worldFilter}
                onSearchTermChange={handleSearchTermChange}
                onHidePastItemsChange={toggleHidePastItems}
                onShowCurrentItemsChange={toggleShowCurrentItems}
                onWorldFilterChange={handleWorldFilterChange}
                className={advancedStyles}
            />
            {noItems ? (
                <div className={advancedStyles.noItemsContainer}>
                    <img 
                        src={noItemsImage} 
                        alt="No items found" 
                        className={advancedStyles.noItemsImage}
                    />
                </div>
            ) : (
                <div>
                    {Object.keys(categorizedItems).map((dateKey) => (
                        <div key={dateKey}>
                            <h2 
                                className={advancedStyles.categoryHeader}
                                onClick={() => toggleCategory(dateKey)}
                            >
                                <span className={advancedStyles.categoryDate}>
                                    {formatDate(dateKey)}
                                </span>
                                <span className={advancedStyles.categoryToggle}>
                                    {collapsedCategories[dateKey] ? '▶' : '▼'}
                                </span>
                            </h2>
                            {!collapsedCategories[dateKey] && (
                                <ul className={advancedStyles.itemList}>
                                    {categorizedItems[dateKey].map(({ key, item }) => (
                                        <AdvancedItemCard
                                            key={key}
                                            itemKey={key}
                                            item={item}
                                            isOpen={openItemId === item}
                                            onItemClick={() => handleItemClick(item)}
                                            isTouchDevice={isTouchDevice}
                                        />
                                    ))}
                                </ul>
                            )}
                        </div>
                    ))}
                </div>
            )}
            <Footer />
        </div>
    );
}

export default AdvancedItemList;
