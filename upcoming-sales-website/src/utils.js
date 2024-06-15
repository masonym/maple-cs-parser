import React from 'react';

// Function to format numbers using the Internationalization API
export const formatNumber = (number) => new Intl.NumberFormat('en-US').format(number);

// Function to convert newlines to <br /> elements
export const convertNewlinesToBreaks = (text) => {
    if (!text) return null;
    return text.split('\n').map((line, index) => (
        <React.Fragment key={index}>
            {line}
            <br />
        </React.Fragment>
    ));
};

// Function to format dates in a more reliable way
export const formatDate = (dateString) => {
    // Use a more reliable way to parse the date string
    const date = new Date(Date.parse(dateString));

    const daysOfWeek = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    const monthsOfYear = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

    const dayOfWeek = daysOfWeek[date.getUTCDay()];
    const month = monthsOfYear[date.getUTCMonth()];
    const dayOfMonth = date.getUTCDate();
    const year = date.getUTCFullYear();

    const daySuffix = (day) => {
        if (day > 3 && day < 21) return 'th';  // Handle special case for 11-13th
        switch (day % 10) {
            case 1: return "st";
            case 2: return "nd";
            case 3: return "rd";
            default: return "th";
        }
    };

    return `${dayOfWeek}, ${month} ${dayOfMonth}${daySuffix(dayOfMonth)}, ${year}`;
}
