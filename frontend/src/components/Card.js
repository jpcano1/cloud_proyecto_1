
import React from "react";
import {Button, Modal} from 'react-bootstrap';


export default function Card(props) {
  return (
<div className="card" style={{width: "18rem"}}>
<img className="card-img-top" src="" alt={props.contest.name}/>
    <div className="card-body">
        <h5 className="card-title">{props.contest.name}</h5>
        <Button variant="danger">Editar</Button>
        <Button variant="info">Eliminar</Button>
    </div>
</div>  
  );
}