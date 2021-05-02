import axios from "axios";



const url = process.env.REACT_APP_API_URL+ process.env.REACT_APP_PORT+ "/api/voice"
const urlUpload = process.env.REACT_APP_API_URL+ process.env.REACT_APP_PORT + "/api/voice_upload"

export async function get_voice_detail(id){
    let answer = await axios.get(url+"/"+id); 
    return answer.data; 
}
export async function get_voices(id,page=1){
    let answer = await axios.get(url,{ params: { contest_url: id, page: page }}); 
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
