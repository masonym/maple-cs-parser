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
    // Split the dateString to avoid timezone issues in Safari
    const [year, month, day] = dateString.split('-');
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

export function formatSaleTimesDate(dateString) {
    // Split the input date string by space to separate date and time
    let [datePart, timePart] = dateString.split(' ');
  
    // Split the date part by '-' to get the components of the date
    let [month, day, year] = datePart.split('-');
  
    // Format the year to be in two digits
    year = year.slice(2);
  
    // Combine the parts into the desired format
    let formattedDate = `${month}/${day}/${year} ${timePart}`;
  
    return formattedDate;
  }

export function calculateDateDifference(date1, date2) {
  // Function to parse date strings into Date objects
  function parseDate(dateString) {
    // Check if the date string is in ISO 8601 format
    const isoFormat = /^\d{4}-\d{2}-\d{2}$/;
    if (isoFormat.test(dateString)) {
      return new Date(dateString);
    }

    // Try to parse other common date formats (e.g., MM/DD/YYYY or DD/MM/YYYY)
    const parts = dateString.split(/[\/\-\s]/);
    if (parts.length === 3) {
      let year, month, day;
      if (parts[0].length === 4) { // YYYY-MM-DD
        year = parseInt(parts[0], 10);
        month = parseInt(parts[1], 10) - 1;
        day = parseInt(parts[2], 10);
      } else if (parts[2].length === 4) { // MM/DD/YYYY or DD/MM/YYYY
        year = parseInt(parts[2], 10);
        if (parseInt(parts[0], 10) > 12) { // DD/MM/YYYY
          day = parseInt(parts[0], 10);
          month = parseInt(parts[1], 10) - 1;
        } else { // MM/DD/YYYY
          month = parseInt(parts[0], 10) - 1;
          day = parseInt(parts[1], 10);
        }
      }
      return new Date(year, month, day);
    }

    // Fallback to creating a new Date object directly
    return new Date(dateString);
  }

  // Parse the date strings into Date objects
  let dateObj1 = parseDate(date1);
  let dateObj2 = parseDate(date2);

  // Check if the dates are valid
  if (isNaN(dateObj1) || isNaN(dateObj2)) {
    throw new Error("Invalid date format");
  }

  // Calculate the difference in milliseconds
  let differenceInMillis = dateObj2 - dateObj1;

  // Convert the difference from milliseconds to days
  let differenceInDays = Math.floor(differenceInMillis / (1000 * 60 * 60 * 24));

  let daysText = "";
  if (differenceInDays > 1) {
    daysText = `${differenceInDays} days`;
  } else if (differenceInDays === 1) {
    daysText = `${differenceInDays} day`;
  } else {
    daysText = `0 days`; // In case the difference is less than a day
  }

  return daysText;
}

  