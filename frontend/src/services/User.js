import axios from "axios";
import Cookie from "js-cookie";

const url = "http://localhost:5000/api"

export async function post_login(data){
   axios.post(url+"/login",data).then((datar) => {
       Cookie.set("access_token",datar.data.access_token);
   });
}
export async function post_register(data){
    axios.post(url + "/usuarios",data).then(() => {
        console.log("registrado");
    });
 }