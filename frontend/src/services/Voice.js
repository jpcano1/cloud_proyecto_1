import axios from "axios";


const url = "http://localhost:5000/api/voice"
const urlUpload = "http://localhost:5000/api/voice_upload"


export async function get_voice_detail(id){
    let answer = await axios.get(url+"/"+id); 
    return answer.data; 
}
export async function get_voices(){
    let answer = await axios.get(url); 
    return answer.data.voices; 
}
export async function post_voice(data){
    let answer = await axios.post(url,data); 
    return answer.data.voice; 
}
export async function upload_voice(id,data){
    let answer = await axios.post(urlUpload+"/"+id,data); 
    return answer.data; 
}