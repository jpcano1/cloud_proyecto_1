import React from 'react'
import { makeStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import { Carousel } from 'react-bootstrap';
import Carousel1 from '../images/Carousel 1.jpg';
import Carousel2 from '../images/Carousel 2.jpg';
import Logo from '../images/Logo SuperVoices.png';

export default function Landing(){

    // var pad = {
    //     paddingHorizontal: 100
    // }

    return(<div
        className = "mx-auto"
        style = {{paddingLeft : 175,  paddingRight: 175}}
    >

        <Carousel>
  <Carousel.Item>
    <img
      src={Carousel1}
      alt="First slide"
      width= "95%"
      className = "rounded mx-auto d-block"
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
      width= "95%"
      className = "rounded mx-auto d-block"
    />
    <Carousel.Caption>
      <h3>Por qué elegirnos</h3>
      <p>Somos un proveedor de SaaS desde la nube, ofrecemos seguridad, desempeño y facilidad para realizar los concursos todo usando tecnologías Cloud.</p>
    </Carousel.Caption>
  </Carousel.Item>
</Carousel>
    </div>)
}