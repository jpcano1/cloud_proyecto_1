
import React, {useEffect,useState} from 'react';
import {get_contest_detail} from '../services/Contest'
import {Button, Modal, Form} from 'react-bootstrap';


export default function Contest(props){
    const[contest, setContest] = useState([]);
    const[showModalUpload,setShowModalUpload ] = useState(false);
    const[voiceSelected, setVoiceSelected] = useState([]);
    const[name, setName] = useState([]);
    const[lasName, setLastName] = useState([]);
    const[email, setEmail] = useState([]);
    const[voice, setVoice] = useState([]); 

    useEffect(async () =>{
        let answer = await get_contest_detail(props.match.params.url)
        console.log(answer);
        setContest(answer.contest); 
    },[contest.id])

    function validateForm(){
        return email.length > 0 && name.length > 0 & lasName.length > 0 && voice
    }

    function uploadVoice(){
        
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
                      <label htmlfor="inputName">Name</label>
                      <input
                        type="text"
                        className="form-control"
                        id="inputName"
                        onChange={(e) => setName(e.target.value)}
                        required
                      />
                    </div>
                    <div className="form-group">
                      <label htmlfor="inputQuantity">Last Name</label>
                      <input
                        type="text"
                        className="form-control"
                        onChange={(e) => setLastName(e.target.value)}
                        required
                      />
                    </div>
                    <div className="form-group">
                      <label htmlfor="inputPrice">Email</label>
                      <input
                        type="email"
                        className="form-control"
                        onChange={(e) => setEmail(e.target.value)}
                        required
                      />
                    </div>
                    <div className="form-group">
                      <label htmlfor="inputType">Voice</label>
                      <input
                        type="file"
                        className="form-control-file"
                        onChange={(e) => setVoice(e.target.files[0])}
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
                    onClick={() => uploadVoice()}
                  >
                    Submit
              </button>
                </div>
              </div>
            </Modal>


    </div>
    )

}