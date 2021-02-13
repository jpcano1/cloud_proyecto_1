import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import Login from './components/Login';
import Landing from './components/Landing'; 
import NavBar from './components/Navbar';
import AdminMenu from './components/AdminMenu';
import SignUp from './components/SignUp'; 
import Contest from './components/Contest';
import reportWebVitals from './reportWebVitals';
import { BrowserRouter, Route, Switch } from "react-router-dom";
import 'bootstrap/dist/css/bootstrap.min.css';

ReactDOM.render(
  <React.StrictMode>
      <BrowserRouter>
      <NavBar/>
        <Switch>
          <Route exact path = "/" component={Landing}/>
          <Route exact path = "/login" component={Login}/>
          <Route exact path = "/signUp" component = {SignUp} />
          <Route exact path = "/contest" component = {AdminMenu} />
          <Route exact path = "/contest/:url" component = {Contest} />
        </Switch>
      </BrowserRouter>
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
