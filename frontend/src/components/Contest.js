
import React, {useEffect,useState} from 'react';
import {get_contest_detail} from '../services/Contest'
import {Button, Modal} from 'react-bootstrap';


export default function Contest(props){
    const[contest, setContest] = useState([]); 

    useEffect(async () =>{
        console.log(props.match.params.url)
        let answer = await get_contest_detail(props.match.params.url)
        console.log(answer); 
        setContest(answer.contest); 
    } )


    return(<div className="container-fluid">
        <div className="row justify-content-center">
            <div className="col-sm-auto">
                <h1>Contest: {contest.name}</h1>
            </div>
        </div>
        <div className= "row justify-content-center">
            <div className="col-sm-6">
                <div className="row">
                    <h4>Prize: {contest.prize} $</h4>
                </div>
                <div className="row">
                    <h4>End Date: {contest.end_date}</h4>
                </div>
                <div className="row">
                     <h4>Begin Date: {contest.begin_date}</h4>
                </div>
            </div>
            <div className="col-sm-6">
                <div className="row">
                    <h4>Script: {contest.script}</h4>
                </div>
                <div className="row">
                    <h4>Recommendations: {contest.recommendations}</h4>
                </div>
            </div>
        </div>
        <div className="row justify-content-center">
            <h2>Do you want to participate?</h2>
        </div>
        <div className="row justify-content-center">
            <Button variant="success">Click Here</Button>
        </div>  

    </div>
    )

}