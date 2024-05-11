// src/index.js
import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import {HelmetProvider} from "react-helmet-async"

ReactDOM.render(
  <BrowserRouter>
  <HelmetProvider>
    <App />

  </HelmetProvider>
  </BrowserRouter>,
  document.getElementById('root')
);