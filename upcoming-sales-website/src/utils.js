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
    // Convert date strings to ISO format if needed
    function toISOFormat(dateString) {
      let date = new Date(dateString);
      if (isNaN(date.getTime())) {
        // Handle invalid date format by converting to ISO
        let parts = dateString.split(/[-\/]/); // Split by '-' or '/'
        if (parts.length === 3) {
          // Assuming the format is MM/DD/YYYY or DD-MM-YYYY
          date = new Date(`${parts[2]}-${parts[0]}-${parts[1]}`);
        }
      }
      return date;
    }
  
    // Parse the date strings into Date objects
    let dateObj1 = toISOFormat(date1);
    let dateObj2 = toISOFormat(date2);
  
    // Validate dates
    if (isNaN(dateObj1.getTime()) || isNaN(dateObj2.getTime())) {
      throw new Error('Invalid date format. Please use a valid date format like YYYY-MM-DD.');
    }
  
    // Calculate the difference in milliseconds
    let differenceInMillis = dateObj2 - dateObj1;
  
    // Convert the difference from milliseconds to days
    let differenceInDays = differenceInMillis / (1000 * 60 * 60 * 24);
  
    // Rounding to nearest integer
    differenceInDays = Math.round(differenceInDays);
  
    let daysText = "";
    if (differenceInDays > 1) {
      daysText = `${differenceInDays} days`;
    } else if (differenceInDays === 1) {
      daysText = "1 day";
    } else if (differenceInDays === 0) {
      daysText = "0 days";
    } else {
      daysText = `${differenceInDays} days`;
    }
  
    return daysText;
  }
  