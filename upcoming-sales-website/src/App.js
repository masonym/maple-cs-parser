// src/App.js
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import HomePage from './Home'
import ItemListMain from './ItemListMain';


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
          <ItemListMain />
        </>
      }
    />
  </Routes>
  );
}

export default App;