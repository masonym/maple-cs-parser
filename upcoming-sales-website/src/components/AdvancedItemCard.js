import React, { useState, useRef, useEffect } from 'react';
import styles from '../assets/AdvancedItemCard.module.css';
import { formatNumber, convertNewlinesToBreaks, formatSaleTimesDate, calculateDateDifference } from '../utils';
import background from '../assets/productBg.png';
import AdvancedItemCardHover from './AdvancedItemCardHover';

const AdvancedItemCard = ({ item }) => {
    const [isHovering, setIsHovering] = useState(false);
    const [hoverPosition, setHoverPosition] = useState({ x: 0, y: 0 });
    const hoverCardRef = useRef(null);
    const positionRef = useRef({ x: 0, y: 0 });

    const handleMouseEnter = () => {
        setIsHovering(true);
    };

    const handleMouseLeave = () => {
        setIsHovering(false);
    };

    const handleMouseMove = (e) => {
        const offsetX = 10;
        const offsetY = 10;
        
        positionRef.current = {
            x: e.pageX + offsetX,
            y: Math.min(e.pageY + offsetY, window.innerHeight + window.scrollY - offsetY)
        };
        
        setHoverPosition(positionRef.current);
    };

    useEffect(() => {
        if (isHovering && hoverCardRef.current) {
            const hoverCardWidth = hoverCardRef.current.offsetWidth;
            const hoverCardHeight = hoverCardRef.current.offsetHeight;

            let newX = positionRef.current.x;
            let newY = Math.min(positionRef.current.y, window.innerHeight + window.scrollY - hoverCardHeight - 10);

            if (newX + hoverCardWidth > window.innerWidth + window.scrollX) {
                newX = positionRef.current.x - hoverCardWidth - 20; // OffsetX * 2
            }

            setHoverPosition({ x: newX, y: newY });
        }
    }, [isHovering]);

    return (
        <li
            className={styles.item}
            onMouseEnter={handleMouseEnter}
            onMouseLeave={handleMouseLeave}
            onMouseMove={handleMouseMove}
        >
            <li key={item.itemID} className={styles.item}>
                <div className={styles.itemFlexContainer} style={{ backgroundImage: `url(${background})` }}>
                    <img
                        src={`./images/${item.itemID}.png`}
                        className={styles.itemImage}
                        alt={item.name}
                        onError={(e) => { e.target.style.display = 'none'; }}
                    />
                    <div className={styles.itemDetails}>
                        <p className={styles.itemName}>{item.name}{item.count > 1 ? ` (x${item.count})` : ''}</p>
                        <p className={styles.itemPrice}>{formatNumber(item.price)} NX</p>
                    </div>
                </div>
            </li>
            {isHovering && (
                <AdvancedItemCardHover item={item} position={hoverPosition} hoverCardRef={hoverCardRef} />
            )}
        </li>
    );
};

export default AdvancedItemCard;
