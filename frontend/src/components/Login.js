import React,{useState} from 'react'
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import {post_login} from '../services/User';
import { useHistory, Link } from "react-router-dom";
import '../css/LoginCss.css'

export default function Login(){
    const history = useHistory();
    const [email, setEmail] = useState([]);
    const [password, setPassword] = useState([]);

    function validateForm() {
      return email.length > 0 && password.length > 0;
    }
  
    async function handleSubmit(event) {
      event.preventDefault();
      let data = {"email": email, "password":password}; 
      let answer = await post_login(data);
      history.push({pathname:"/contest", state: { admin: answer }});
    }
    return(
        <div className="Login justify-content-center center text-center col-4">
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
    </div>
    )
}