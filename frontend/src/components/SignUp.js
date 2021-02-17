import React,{useState} from 'react'
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import {post_register} from '../services/User';
import { useHistory } from "react-router-dom";
import '../css/LoginCss.css';
import Snackbar from '@material-ui/core/Snackbar';
import MuiAlert from '@material-ui/lab/Alert';

export default function SignUp(){
    const history = useHistory();
    const[name, setName] = useState("");
    const[last_name, setLastName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const[confirmPassword, setConfirmPassword] = useState("");

    const[openBar, setOpenBar] = useState(false);
    const[message,setMessage] = useState(""); 

    function validateForm() {
      return email.length > 0 && password.length > 0 && password == confirmPassword;
    }
    function handleClose (event, reason){
      if (reason === 'clickaway') {
        return;
      }
  
      setOpenBar(false);
    }
  
    async function handleSubmit(event) {
      event.preventDefault();
      let newAdmin = new Object(); 
      newAdmin.name = name; 
      newAdmin.last_name = last_name; 
      newAdmin.email = email; 
      newAdmin.password = password;
      try{
        await post_register(newAdmin);
        history.push("/login");
      }
      catch(error){
        if(error.response){
          setMessage(error.response.data.errors);
          setOpenBar(true);
        }
        else
        {
          setMessage(error.message);
        }
      }

    }
    return(
        <div className="Login justify-content-center center col-4">
        <Form onSubmit={handleSubmit}>
        <Form.Group size="lg" controlId="name">
          <Form.Label>Name</Form.Label>
          <Form.Control
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </Form.Group>
        <Form.Group size="lg" controlId="lastName">
          <Form.Label>Last Name</Form.Label>
          <Form.Control
            type="text"
            value={last_name}
            onChange={(e) => setLastName(e.target.value)}
          />
        </Form.Group>
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
        <Form.Group size="lg" controlId="confirmPassword">
          <Form.Label>Confirm Password</Form.Label>
          <Form.Control
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
          />
          
        </Form.Group>
        <Button block size="lg" type="submit" disabled={!validateForm()}>
          Register
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