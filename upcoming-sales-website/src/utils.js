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