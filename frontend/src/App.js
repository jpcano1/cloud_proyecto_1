import logo from './logo.svg';
import './App.css';
import Login from './components/Login';
import Landing from './components/Landing'; 
import NavBarr from './components/Navbar';
import AdminMenu from './components/AdminMenu';
import SignUp from './components/SignUp'; 
import Contest from './components/Contest';
import { BrowserRouter, Route, Switch } from "react-router-dom";

function App() {
  return (
    <BrowserRouter>
      <main>
        <NavBarr/>
        <Switch>
          <Route exact path = "/" component={Landing}/>
          <Route exact path = "/login" component={Login}/>
          <Route exact path = "/signUp" component = {SignUp} />
          <Route exact path = "/contest" component = {AdminMenu} />
          <Route exact path = "/contest/:url" component = {Contest} />
        </Switch>
      </main>
    </BrowserRouter>
  );
}

export default App;
