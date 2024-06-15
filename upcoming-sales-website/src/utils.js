import React from 'react';

export const formatNumber = (number) => new Intl.NumberFormat('en-US').format(number);

export const convertNewlinesToBreaks = (text) => {
    if (!text) return null;
    return text.split('\n').map((line, index) => (
        <React.Fragment key={index}>
            {line}
            <br />
        </React.Fragment>
    ));
};

export const formatDate = (dateString) => {
    if (!dateString) return 'Invalid Date';

    // Manually parse the date string to avoid issues with Safari's date parsing
    const [year, month, day] = dateString.split('-').map(Number);
    if (isNaN(year) || isNaN(month) || isNaN(day)) return 'Invalid Date';
    
    const date = new Date(Date.UTC(year, month - 1, day));

    const daysOfWeek = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    const monthsOfYear = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

    const dayOfWeek = daysOfWeek[date.getUTCDay()];
    const monthName = monthsOfYear[date.getUTCMonth()];
    const dayOfMonth = date.getUTCDate();
    const yearNumber = date.getUTCFullYear();

    const daySuffix = (day) => {
        if (day > 3 && day < 21) return 'th';  // Handle special case for 11-13th
        switch (day % 10) {
            case 1: return "st";
            case 2: return "nd";
            case 3: return "rd";
            default: return "th";
        }
    };

    return `${dayOfWeek}, ${monthName} ${dayOfMonth}${daySuffix(dayOfMonth)}, ${yearNumber}`;
}
