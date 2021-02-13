
import React, {useEffect} from 'react';
import {get_contest_detail} from '../services/Contest'


export default function Contest(props){

    useEffect(() =>{
        console.log(props.match.params.url)
        get_contest_detail(props.match.params.url)

    } )


    return(<div>
        <h1>Contest Detail</h1>
    </div>)
}