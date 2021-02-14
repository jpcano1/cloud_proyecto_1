import axios from "axios";
import Cookie from 'js-cookie';


const url = "http://localhost:5000/api/contest"
const urlBanner = "http://localhost:5000/api/banner"

export async function get_contest_detail(id){
    let answer = await axios.get(url+"/"+id); 
    return answer.data; 
}

export async function upload_banner(id, data){
    axios.defaults.headers.common['Authorization'] = 
    'Bearer ' + Cookie.get("access_token");
    let answer = await axios.post(urlBanner+"/"+id,data); 
    return answer.data; 
}

export async function post_contest(data){
    axios.defaults.headers.common['Authorization'] = 
    'Bearer ' + Cookie.get("access_token");
    let answer = await axios.post(url,data); 
    return answer.data; 
}


export async function delete_contest(data){
    axios.defaults.headers.common['Authorization'] = 
    'Bearer ' + Cookie.get("access_token");
    let answer = await axios.delete(url+"/"+data); 
    return answer.data; 
}

export async function put_contest(data){
    axios.defaults.headers.common['Authorization'] = 
    'Bearer ' + Cookie.get("access_token");
    let urltemp = url+"/"+data.url; 
    let answer = await axios.put(urltemp, data);

    console.log(answer);
    return answer.data; 
}

export async function get_contests(){
    let answer =  await axios.get(url);
    let contestArray = answer.data.contests;
    return contestArray
}
