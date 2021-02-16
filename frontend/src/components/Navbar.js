import React,{useEffect, useState} from 'react';
import {Link} from "react-router-dom";
import { Navbar,Button,Nav } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import '../css/NavbarCss.css'
import Cookie from "js-cookie";


export default function NavbarO(){

    const [isLogged,setLogged] = useState(false); 

    useEffect(() => {
        let token = Cookie.get("access_token"); 
        if(token){
            setLogged(true)
        }
    },[])

    function logOut(){
        Cookie.remove('access_token');
        Cookie.remove('admin');
    }


    return( 
        <Navbar bg="dark" variant="dark">
            <Navbar.Brand href="/">
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
            {isLogged && <Link to="/contest" >My Contests</Link>}
        </Nav>
        <div className="button-space">
        {isLogged? <Button variant="outline-info" href="/">Home</Button>
        : <Button variant="outline-info" href="/login">Login</Button>
        }
        
        </div>
        <div  className="button-space">
        {isLogged? <Button variant="outline-info" href="/" onClick={() => logOut()}>Log Out</Button>
        : <Button variant="outline-info" href="/signup">Sign Up</Button>
        }
        </div>
      </Navbar>)    
}   