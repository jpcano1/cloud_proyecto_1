import React,{useState} from 'react'
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import {post_login} from '../services/User';
import { useHistory, Link } from "react-router-dom";
import '../css/LoginCss.css'; 
import Snackbar from '@material-ui/core/Snackbar';
import MuiAlert from '@material-ui/lab/Alert';
import Cookie from 'js-cookie';
var Memcached = require('memcached-promise'); 
var memcached = new Memcached('cloudmemcache.6b8rab.0001.use1.cache.amazonaws.com:11211');
const TIME = 7200

export default function Login(){
    const history = useHistory();
    const [email, setEmail] = useState([]);
    const [password, setPassword] = useState([]);

    const[openBar, setOpenBar] = useState(false);
    const[message,setMessage] = useState(""); 
  
    function handleClose (event, reason){
      if (reason === 'clickaway') {
        return;
      }
  
      setOpenBar(false);
    }
    function validateForm() {
      return email.length > 0 && password.length > 0;
    }
  
    async function handleSubmit(event) {
      event.preventDefault();
      let data = {"email": email, "password":password}; 
      let answer = await post_login(data);
      if(typeof(answer)==='string'){


          await store('admin',answer)
          Cookie.set('admin', answer);
          history.push({pathname:"/contest"});
      }
      else{
        setMessage(answer); 
        setOpenBar(true);
      }
      
    }
  async function store(key,value){
      try{
          await memcached.set(key,value,TIME)
      }
      catch(error){
          console.log("Ocurrio un error: ", error)
      }
      
  }
  async function getValue(key){
      try{
          return await memcached.get(key);
      }
      catch(error){
          console.log("Ocurrio un error:", error)
      }
  }
    return(
        <div className="Login justify-content-center center  col-4">
        <Form onSubmit={handleSubmit}>
        <Form.Group size="lg" controlId="email">
          <Form.Label>Email</Form.Label>
          <Form.Control
            autoFocus
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </Form.Group>
        <Form.Group size="lg" controlId="password">
          <Form.Label>Password</Form.Label>
          <Form.Control
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </Form.Group>
        <Link to="/SignUp">SignUp</Link>
        <Button block size="lg" type="submit" disabled={!validateForm()}>
          Login
        </Button>
      </Form>
      <Snackbar open={openBar} autoHideDuration={6000} onClose={handleClose}>
      <MuiAlert onClose={handleClose} severity="error">
        {message}
      </MuiAlert>
      </Snackbar>
    </div>
    )
}