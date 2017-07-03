import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import { createStore, applyMiddleware } from 'redux';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import { Link } from 'react-router-dom';
import thunkMiddleware from 'redux-thunk'

import RadioPage from './components/RadioPage'
import rootReducer from './reducers'

import config from './config'
import createWebsocketMiddleware from './middleware/websocket'

let store = createStore(
  rootReducer,
  applyMiddleware(
    createWebsocketMiddleware(config.wsServer),
    thunkMiddleware))

// debug
window.store = store

ReactDOM.render(
  <Provider store={store}>
    <Router>
      <Route path="/" component={RadioPage}/>
    </Router>
  </Provider>,
  document.getElementById('root')
)
