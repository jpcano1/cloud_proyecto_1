import axios from "axios";
import configData from '../config.json';


const url = configData.BACKEND_URL+ "api/voice"
const urlUpload = configData.BACKEND_URL + "api/voice_upload"


export async function get_voice_detail(id){
    let answer = await axios.get(url+"/"+id); 
    return answer.data; 
}
export async function get_voices(id,page=1){
    let answer = await axios.get(url,{ params: { contest_id: id, page: page }}); 
    return answer.data; 
}
export async function post_voice(data){
    let answer = await axios.post(url,data); 
    return answer.data.voice; 
}
export async function upload_voice(id,data){
    let answer = await axios.post(urlUpload+"/"+id,data); 
    return answer.data; 
}