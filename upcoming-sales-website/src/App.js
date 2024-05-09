import React from 'react';
import { Routes, Route } from 'react-router-dom';
import ItemList from './components/ItemList';

function App() {
  return (
    <Routes>
      {/* other routes here */}
      <Route path="/" element={<div>Home Page</div>} />
      {/* Route for ItemList */}
      <Route path="/ms-upcoming-sales" element={<ItemList />} />
    </Routes>
  );
}

export default App;