import axios from "axios";
import Cookie from "js-cookie";
import {store} from './MemCached'; 

const url = process.env.REACT_APP_API_URL + process.env.REACT_APP_PORT + "/api"

export async function post_login(data){
    try{
        let answer = await axios.post(url+"/login",data);
        await store("access_token",answer.data.access_token);
        //Cookie.set("access_token",answer.data.access_token);
        return answer.data.admin_id
    }
    catch (error) {
        // Error 😨
        if (error.response) {
            /*
             * The request was made and the server responded with a
             * status code that falls out of the range of 2xx
             */
            console.log(error.response.data);
            return error.response.data.errors;
        } else if (error.request) {
            /*
             * The request was made but no response was received, `error.request`
             * is an instance of XMLHttpRequest in the browser and an instance
             * of http.ClientRequest in Node.js
             */
            console.log(error.request);
        } else {
            // Something happened in setting up the request and triggered an Error
            console.log('Error', error.message);
        }
        console.log(error);
    }
}
export async function post_register(data){
    axios.post(url + "/signup",data).then(() => {
    });
 }