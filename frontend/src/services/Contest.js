import axios from "axios";
import Cookie from 'js-cookie';


const url = "http://localhost:5000/api/contest"

export async function get_contest_detail(id){

}

export async function post_contest(data){
    axios.defaults.headers.common['Authorization'] = 
    'Bearer ' + Cookie.get("access_token");
    let answer = await axios.post(url,data); 
    return answer.data; 
}

export async function get_contests(){
    let answer =  await axios.get(url);
    let contestArray = answer.data.contests;
    return contestArray
}
