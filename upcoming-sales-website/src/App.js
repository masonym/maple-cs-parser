// src/App.js
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import HomePage from './components/Home'
import ItemList from './components/ItemList';
import { Helmet } from 'react-helmet';


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
  </Routes>
  );
}

export default App;