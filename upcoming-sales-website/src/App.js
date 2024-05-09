// src/App.js
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import ItemList from './components/ItemList';

function App() {
  return (
    <Routes>
      <Route path="/" element={<div>Home Page</div>} />
      <Route path="/ms-upcoming-sales" element={<ItemList />} />
    </Routes>
  );
}

export default App;