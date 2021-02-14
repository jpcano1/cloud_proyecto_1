import React, {useEffect, useState}from 'react'; 
import {Button, Modal} from 'react-bootstrap';
import {get_contests} from '../services/Contest';
import DatePicker from "react-datepicker";
import Card from '../components/Card';


export default function AdminMenu(){
    const [contests, setContest] = useState([]);
    const[contestSelected, setContestSelected] = useState([]); 

    const[name, setName] = useState([]);
    const[banner, setBanner] = useState([]); 
    const[url, setUrl] = useState([]); 
    const[begin_date, setBegin_date] = useState(new Date());
    const[end_date, setEnd_date] = useState(new Date()); 
    const[prize, setPrize] = useState([]); 
    const[script, setScript] = useState([]);
    const[recommendations, setRecommendations] = useState([]);
    const[showCreateModal, setShowCreateModal] = useState(false);
    
    useEffect( ()  => {
        fetchContest()
    },[contests.length])

     async function fetchContest(){
        let answer = await get_contests();
        console.log(answer);
        setContest(answer);
    }

    async function createContest(){
        let newContest = new Object(); 
        newContest.name = name;  
        newContest.url = url; 
        newContest.begin_date = begin_date.getDate() + "/"+ begin_date.getMonth() + "/"+ begin_date.getFullYear();
        newContest.end_date = end_date.getDate() + "/"+ end_date.getMonth() + "/"+ end_date.getFullYear();
        newContest.prize = prize; 
        newContest.script = script; 
        newContest.recommendations = recommendations; 
    }
    return(
    <div className="container-fluid">
        <div className="row justify-content-center">
            <div className="col-sm-auto">
                <h1>Welcome Admin</h1>
            </div>
        </div>
        <div className="row justify-content-center">
            <div className="col-sm-auto">
                <h2>Do you want to create a contest?</h2>
            </div>
        </div>
        <div className="row justify-content-center">
            <div className="col-sm-auto">
                <Button variant="success" onClick={() => setShowCreateModal(true)}>Create Contest</Button>
            </div>
        </div>
        <div className="row">
            <div className="col">
                <h3>Your Contests:</h3>
            </div>
        </div>
        <div className="row justify-content-center">
            <div className="col">
                    {contests.length == 0 && 
                    <h4>You don't have any contest active :(</h4>
                    }
                    {contests.map(h => {return <Card contest={h} key = {h.id}/>})}
            </div>
            
        </div>  

        <Modal show={showCreateModal} idEvent={contestSelected} onHide={() => setShowCreateModal(false)}>
              <div className="modal-content">
                <div className="modal-header">
                  <h5 className="modal-title" id="addProductModalLabel">
                    Create a Contest
              </h5>
                  <button
                    type="button"
                    className="close"
                    data-dismiss="modal"
                    aria-label="Close"
                    onClick={() => setShowCreateModal(false)}
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
                      />
                    </div>
                    <div className="form-group">
                      <label htmlfor="inputType">Banner</label>
                      <input
                        type="text"
                        className="form-control"
                        onChange={(e) => setBanner(e.target.value)}
                      />
                    </div>
                    <div className="form-group">
                      <label htmlfor="inputQuantity">Url</label>
                      <input
                        type="text"
                        className="form-control"
                        onChange={(e) => setUrl(e.target.value)}
                      />
                    </div>
                    <div className="form-group">
                      <label htmlfor="inputPrice">Begin Date</label>
                      <DatePicker selected={begin_date} onChange={date => setBegin_date(date)} dateFormat="yyyy/MM/dd" />
                    </div>
                    <div className="form-group">
                      <label htmlfor="inputPrice">End  Date</label>
                      <DatePicker selected={end_date} onChange={date => setEnd_date(date)} dateFormat="yyyy/MM/dd" />
                    </div>
                    <div className="form-group">
                      <label htmlfor="inputPrice">Prize</label>
                      <input
                        type="number"
                        className="form-control"
                        onChange={(e) => setPrize(e.target.value)}
                      />
                    </div>
                    <div className="form-group">
                      <label htmlfor="inputPrice">Script</label>
                      <input
                        type="text"
                        className="form-control"
                        onChange={(e) => setScript(e.target.value)}
                      />
                    </div>
                    <div className="form-group">
                      <label htmlfor="inputPrice">Recommendations</label>
                      <input
                        type="text"
                        className="form-control"
                        onChange={(e) => setRecommendations(e.target.value)}
                      />
                    </div>
                  </form>
                </div>
                <div className="modal-footer">
                  <button
                    type="button"
                    className="btn btn-danger"
                    data-dismiss="modal"
                    onClick={() => setShowCreateModal(false)}
                  >
                    Cancelar
              </button>
                  <button
                    type="button"
                    className="btn btn-success"
                    onClick={() => createContest()}
                  >
                    Create Constest
              </button>
                </div>
              </div>
            </Modal>
    </div>)
}