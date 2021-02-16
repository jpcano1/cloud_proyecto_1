import axios from "axios";
import Cookie from "js-cookie";

const url = "http://localhost:5000/api"

export async function post_login(data){
    try{
        let answer = await axios.post(url+"/login",data);
        Cookie.set("access_token",answer.data.access_token);
        console.log(answer);
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
            console.log(error.response.status);
            console.log(error.response.headers);
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