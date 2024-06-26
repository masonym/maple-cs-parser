// src/App.js
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import HomePage from './Home'
import ItemList from './ItemList';
import AdvancedItemList from './AdvancedItemList';


function App() {
  return (
    <Routes>
    <Route
      path="/"
      element={
        <>
          <HomePage />
        </>
      }
    />
    <Route
      path="/ms-upcoming-sales"
      element={
        <>
          <ItemList />
        </>
      }
    />
    <Route
      path="/advanced-ms-upcoming-sales"
      element={
        <>
          <AdvancedItemList />
        </>
      }
    />
  </Routes>
  );
}

export default App;