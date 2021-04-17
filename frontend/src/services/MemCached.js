var Memcached = require('memcached-promise'); 
var memcached = new Memcached('cloudmemcache.6b8rab.0001.use1.cache.amazonaws.com:11211')


const TIME = 7200
async function store(key,value){
    try{
        await memcached.set(key,value,TIME)
    }
    catch(error){
        console.log("Ocurrio un error: ", error)
    }
    
}
async function getValue(key){
    try{
        return await memcached.get(key);
    }
    catch(error){
        console.log("Ocurrio un error:", error)
    }
}


