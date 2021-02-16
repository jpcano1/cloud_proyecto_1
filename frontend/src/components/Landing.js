import React,{useState,useEffect} from 'react'
import { makeStyles } from '@material-ui/core/styles';
import {Button} from 'react-bootstrap';
import { Carousel } from 'react-bootstrap';
import Carousel1 from '../images/Carousel 1.jpg';
import Carousel2 from '../images/Carousel 2.jpg';
import Logo from '../images/Logo SuperVoices.png';
import {get_contests} from '../services/Contest';
import '../css/Lading.css';
import configData from '../config.json';

export default function Landing(){


    //URL for request banners
    const urlBanner = configData.BACKEND_URL;
    // var pad = {
    //     paddingHorizontal: 100
    // }
    const[contests, setContests] = useState([]); 
    useEffect(() => {
      fetchContests();

    },[]);

    async function fetchContests(){
      let answer = await get_contests();
      setContests(answer);
    }
    return(<div
        className = "carrusel-container"
        style = {{paddingLeft : 0,  paddingRight: 0}}
    >

        <Carousel>
  <Carousel.Item>
    <img
      src={Carousel1}
      alt="First slide"
      width= "100%"
      className = "rounded d-block carrusel-container"
    />

    <Carousel.Caption>
      <h3>Quiénes somos</h3>
      <p>SuperVoices es una compañía que ofrece su servicio web para realizar concursos de pequeñas, medianas y grandes empresas que buscan actores de voz para sus anuncios publicitarios. </p>
    </Carousel.Caption>
  </Carousel.Item>
  <Carousel.Item >
    <img
      src={Carousel2}
      alt="Second slide"
      width= "100%"
      className = "rounded d-block carrusel-container"
    />
    <Carousel.Caption>
      <h3>Por qué elegirnos</h3>
      <p>Somos un proveedor de SaaS desde la nube, ofrecemos seguridad, desempeño y facilidad para realizar los concursos todo usando tecnologías Cloud.</p>
    </Carousel.Caption>
  </Carousel.Item>
</Carousel>
    <h3 className="m-2">Active Contests:</h3>
    <div className="row m-2">
    {contests.map(h => 
                      {return <div className="card m-2" style={{width: "18rem"}}>
                        <div>
                              <img className="card-img-top img-fluid img-size" src={urlBanner+h.banner} alt={h.name}/>
                        </div>
                        
                            <div className="card-body">
                                <h5 className="card-title">{h.name}</h5>
                                <Button className="m-1" variant="outline-info" href={'/contest/' + h.url}>Details</Button>
                            </div>
                        </div>})}
    </div>
  </div>)
}