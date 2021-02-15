import axios from "axios";


const url = "http://localhost:5000/api/voice"
const urlUpload = "http://localhost:5000/api/voice_upload"

export async function get_voice_detail(id){
    let answer = await axios.get(url+"/"+id); 
    return answer.data; 
}