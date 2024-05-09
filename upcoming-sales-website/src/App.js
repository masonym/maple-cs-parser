import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Home from './components/Home';
import ItemList from './components/ItemList';

function App() {
  return (
    <Router basename="/xyz">  // Adjust the basename according to your deployment subpath
      <Switch>
        <Route exact path="/" component={Home} />
        <Route path="/ms-upcoming-sales" component={ItemList} />
      </Switch>
    </Router>
  );
}

export default App;