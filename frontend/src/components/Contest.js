
import React, {useEffect,useState} from 'react';
import {get_contest_detail} from '../services/Contest';
import {post_voice,upload_voice,get_voices} from '../services/Voice';
import {Button, Modal} from 'react-bootstrap';
import Pagination from '@material-ui/lab/Pagination';


export default function Contest(props){
    const[contest, setContest] = useState([]);

    const[showModalUpload,setShowModalUpload ] = useState(false);

    const[voiceSelected, setVoiceSelected] = useState([]);

    const[name, setName] = useState([]);
    const[lastName, setLastName] = useState([]);
    const[email, setEmail] = useState([]);
    const[voice, setVoice] = useState([]); 
    const[observations, setObservations] = useState([]);
    const[audios,setAudios] = useState([]);

    const[minValue,setMinValue] = useState(0); 
    const[maxValue,setMaxValue] = useState(50); 

    useEffect(async () =>{
        let answer = await get_contest_detail(props.match.params.url)
        setContest(answer.contest); 
        answer = await get_voices(); 
        setAudios(answer);
    },[contest.id])

    function validateForm(){
        return email.length > 0 && name.length > 0 & lastName.length > 0 && voice
    }
    function handlePagination(event, value){
        console.log(value); 
        setMinValue(maxValue); 
        setMaxValue(value*50);
    }
    async function createVoice(){
        let newVoice = new Object(); 
        newVoice.name = name; 
        newVoice.last_name = lastName; 
        newVoice.email = email; 
        newVoice.observations = observations;
        newVoice.contest = contest.id;
        console.log(newVoice);
        let answer = await post_voice(newVoice); 
        await uploadVoice(answer.id)
        setShowModalUpload(false);
    }
    async function uploadVoice(id){
        const fd = new FormData();
        fd.append('audio', voice); 
        await upload_voice(id, fd)
    }

    return(<div className="container-fluid">
        <div className="row justify-content-center">
            <div className="col-sm-auto">
                <h1>Contest: {contest.name}</h1>
            </div>
        </div>
        <div className= "container-fluid row justify-content-center">
            <div className="col-sm-6">
                <div className="row">
                    <h4>Prize: {contest.prize} $</h4>
                </div>
                <div className="row">
                    <h4>End Date: {contest.end_date}</h4>
                </div>
                <div className="row">
                     <h4>Begin Date: {contest.begin_date}</h4>
                </div>
            </div>
            <div className="col-sm-6">
                <div className="row">
                    <h4>Script: {contest.script}</h4>
                </div>
                <div className="row">
                    <h4>Recommendations: {contest.recommendations}</h4>
                </div>
            </div>
        </div>
        <div className="row justify-content-center">
            <h2>Do you want to participate?</h2>
        </div>
        <div className="row justify-content-center">
            <Button variant="success" onClick= {() => setShowModalUpload(true)}>Click Here</Button>
        </div> 
        <div className="Voices">
            <h3>Voices:</h3>
        </div>
        <div className="container row">
                    {audios.length == 0 && 
                    <h4>Nobody has participated </h4>
                    }
                    {audios.slice(minValue, maxValue).map(h => 
                      {return <div className="card m-2" style={{width: "18rem"}}>
                            <div className="card-body">
                                <h5 className="card-title">{h.name}</h5>
                            </div>
                            <div className="card-footer">
                                <h5 >{h.observations}</h5>
                            </div>
                        </div>})}
        </div> 
        <div className="row justify-content-center">
                    <Pagination
                        variant="outlined" color="primary"
                        defaultCurrent={1}
                        onChange={handlePagination}
                        count={audios.length}
                    />
         </div>
        
        <Modal show={showModalUpload} onHide={() => setShowModalUpload(false)}>
              <div className="modal-content">
                <div className="modal-header">
                    <h5 className="modal-title" id="addProductModalLabel">
                        Upload your Voice
                    </h5>
                    <button
                        type="button"
                        className="close"
                        data-dismiss="modal"
                        aria-label="Close"
                        onClick={() => setShowModalUpload(false)}
                    >
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div className="modal-body">
                  <form>
                    <div className="form-group">
                      <label id="inputName">Name</label>
                      <input
                        type="text"
                        className="form-control"
                        id="inputName"
                        onChange={(e) => setName(e.target.value)}
                        required
                      />
                    </div>
                    <div className="form-group">
                      <label id="inputQuantity">Last Name</label>
                      <input
                        type="text"
                        className="form-control"
                        onChange={(e) => setLastName(e.target.value)}
                        required
                      />
                    </div>
                    <div className="form-group">
                      <label id="inputPrice">Email</label>
                      <input
                        type="email"
                        className="form-control"
                        onChange={(e) => setEmail(e.target.value)}
                        required
                      />
                    </div>
                    <div className="form-group">
                      <label id="inputType">Voice</label>
                      <input
                        type="file"
                        className="form-control-file"
                        onChange={(e) => setVoice(e.target.files[0])}
                        required
                      />
                    </div>
                    <div className="form-group">
                      <label id="inputObservations">Observations</label>
                      <input
                        type="text"
                        className="form-control"
                        onChange={(e) => setObservations(e.target.value)}
                        required
                      />
                    </div>
                  </form>
                </div>
                <div className="modal-footer">
                  <button
                    type="button"
                    className="btn btn-danger"
                    data-dismiss="modal"
                    onClick={() => setShowModalUpload(false)}
                  >
                    Cancel
              </button>
                  <button
                    type="button"
                    className="btn btn-success"
                    onClick={() => createVoice()}
                  >
                    Submit
              </button>
                </div>
              </div>
            </Modal>


    </div>
    )

}