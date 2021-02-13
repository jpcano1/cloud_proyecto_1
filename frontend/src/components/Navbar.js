import React from 'react';
import {Link} from "react-router-dom";
import { Navbar,Button,FormControl,Form,Nav } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import '../css/NavbarCss.css'


export default function NavbarO(){


    return( 
        <Navbar bg="dark" variant="dark">
            <Navbar.Brand href="#home">
                <img
                    src="https://avmusicacademy.org/sites/default/files/microphone.png"
                    width="30"
                    height="30"
                    className="d-inline-block align-top"
                    alt="logo"
                />
            </Navbar.Brand>
        <Navbar.Brand href="/">SuperVoices</Navbar.Brand>
        <Nav className="mr-auto">
        </Nav>
        <div className="button-space">
        <Button variant="outline-info" href="/login">Login</Button>
        </div>
        <div  className="button-space">
        <Button variant="outline-info" href="/signup">SignUp</Button>
        </div>
      </Navbar>)    
}   