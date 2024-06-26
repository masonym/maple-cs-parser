import React, { useState, useRef, useEffect } from 'react';
import styles from '../assets/AdvancedItemCard.module.css';
import { formatNumber } from '../utils';
import background from '../assets/productBg.png';
import AdvancedItemCardHover from './AdvancedItemCardHover';

const AdvancedItemCard = ({ itemKey, item, isOpen, onItemClick, isTouchDevice }) => {
    const [isHovering, setIsHovering] = useState(false);
    const [hoverPosition, setHoverPosition] = useState({ x: 0, y: 0 });
    const hoverCardRef = useRef(null);

    const handleMouseEnter = () => {
        if (!isTouchDevice) {
            setIsHovering(true);
        }
    };

    const handleMouseLeave = () => {
        if (!isTouchDevice) {
            setIsHovering(false);
        }
    };

    const handleMouseMove = (e) => {
        if (!isTouchDevice) {
            updateHoverPosition(e.pageX, e.pageY);
        }
    };

    const handleClick = (e) => {
        if (isTouchDevice) {
            e.preventDefault();
            e.stopPropagation();  // Stop the event from bubbling up to the parent elements
            onItemClick();
        }
    };

    const updateHoverPosition = (pageX, pageY) => {
        const hoverCardWidth = hoverCardRef.current ? hoverCardRef.current.offsetWidth : 0;
        const hoverCardHeight = hoverCardRef.current ? hoverCardRef.current.offsetHeight : 0;
        const offsetX = 10;
        const offsetY = 10;

        let newX = pageX + offsetX;
        const newY = Math.min(pageY + offsetY, window.innerHeight + window.scrollY - hoverCardHeight - offsetY);

        if (newX + hoverCardWidth > window.innerWidth + window.scrollX) {
            newX = pageX - hoverCardWidth - offsetX;
        }

        setHoverPosition({ x: newX, y: newY });
    };

    return (
        <li
            className={styles.item}
            onMouseEnter={handleMouseEnter}
            onMouseLeave={handleMouseLeave}
            onMouseMove={handleMouseMove}
            onClick={handleClick}
        >
            <div className={styles.itemFlexContainer} style={{ backgroundImage: `url(${background})` }}>
                <img
                    src={`./images/${item.itemID}.png`}
                    className={styles.itemImage}
                    alt={item.name}
                    onError={(e) => { e.target.style.display = 'none'; }}
                />
                <div className={styles.itemDetails}>
                    <p className={styles.itemName}>{item.name}{item.count > 1 ? ` (x${item.count})` : ''}</p>
                    <p className={styles.itemPrice}>
                        {formatNumber(item.price)}
                        {itemKey.toString().startsWith('870') ? ' Mesos' : ' NX'}
                        {item.discount == 1 ? <><br /><s>{formatNumber(item.originalPrice)}{itemKey.toString().startsWith('870') ? ' Mesos' : ' NX'}</s></> : ''}
                    </p>

                </div>
            </div>
            {(isHovering || (isTouchDevice && isOpen)) && (
                <AdvancedItemCardHover
                    itemKey={itemKey}
                    item={item}
                    position={hoverPosition}
                    isTouchDevice={isTouchDevice}
                    hoverCardRef={hoverCardRef}
                    onClose={onItemClick}
                />
            )}
        </li>
    );
};

export default AdvancedItemCard;