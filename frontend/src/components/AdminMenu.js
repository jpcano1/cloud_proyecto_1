import React, {useEffect, useState}from 'react'; 
import {Button, Modal} from 'react-bootstrap';
import {get_contests_admin, post_contest, delete_contest,put_contest, upload_banner} from '../services/Contest';
import Snackbar from '@material-ui/core/Snackbar';
import MuiAlert from '@material-ui/lab/Alert';
import Cookie from 'js-cookie';
import { useHistory } from "react-router-dom";


export default function AdminMenu(){
    //URL for request banners
    const urlBanner = process.env.REACT_APP_API_URL+ process.env.REACT_APP_PORT;
    //Contest and Selected Contest
    const [contests, setContest] = useState([]);
    const[contestSelected, setContestSelected] = useState([]); 
    //Atributtes for Contest
    const[name, setName] = useState("");
    const[banner, setBanner] = useState(""); 
    const[url, setUrl] = useState(""); 
    const[begin_date, setBegin_date] = useState(new Date());
    const[end_date, setEnd_date] = useState(new Date()); 
    const[prize, setPrize] = useState(""); 
    const[script, setScript] = useState("");
    const[recommendations, setRecommendations] = useState("");
    //Modals
    const[showCreateModal, setShowCreateModal] = useState(false);
    const[showEditModal, setShowEditModal] = useState(false);
    const[showDeleteModal, setShowDeleteModal] = useState(false);
    //Message and Snackbar to handle error messages  
    const[message, setMessage] = useState("Something went wrong, ups");
    const[errorModal, setErrorModal] = useState(false);
    //Manage redirects
    const history = useHistory();
    //
    const[dateChange,setDateChange] = useState(false);
    
    useEffect(async ()  => {
        await fetchContest()
    },[contests.length])

     async function fetchContest(){
       if(Cookie.get('admin')===undefined){
        history.push("/login");
       }
        let answer = await get_contests_admin(Cookie.get('admin'));
        setContest(answer);
    }
    function handleClose (event, reason){
      if (reason === 'clickaway') {
        return;
      }
  
      setErrorModal(false);
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

        try{
          let answer = await post_contest(newContest);
          if(banner){
            fileUpload(answer.contest.id)
          }
          setShowCreateModal(false);
          fetchContest(); 
        }
        catch(error){
            if (error.response) {
              /*
              * The request was made and the server responded with a
              * status code that falls out of the range of 2xx
              */
              setMessage(error.response.data.errors);
              setErrorModal(true);
          } 
          else{
              setMessage(error.message)
              setErrorModal(true);
          }
        }
    }
    
    async function deleteContest(url){
      await delete_contest(url);
      setShowDeleteModal(false);
      fetchContest();
    }
    async function editContest(){
      let newContest = new Object();
      if(name){
        newContest.name = name;  
      }
       
        newContest.url = contestSelected.url;

      if(dateChange){
        newContest.begin_date = begin_date.getDate() + "/"+ begin_date.getMonth() + "/"+ begin_date.getFullYear();
        newContest.end_date = end_date.getDate() + "/"+ end_date.getMonth() + "/"+ end_date.getFullYear();
      }

      if(banner){
        await fileUpload(contestSelected.id);
      }
      if(prize){
        newContest.prize = prize; 
      }
      if(script){
        newContest.script = script;
      }
      if(recommendations){
        newContest.recommendations = recommendations; 

      }
      try{
          await put_contest(newContest); 
          setShowEditModal(false);
          fetchContest();
      }
      catch(error){
        if (error.response) {
          /*
          * The request was made and the server responded with a
          * status code that falls out of the range of 2xx
          */
          setMessage(error.response.data.errors);
          setErrorModal(true);
      } 
      else{
          setMessage(error.message)
          setErrorModal(true);
      }
      }
    }
    async function fileUpload(id){
      const fd = new FormData();
      fd.append('banner', banner); 
      await upload_banner(id, fd)
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
        <div className="container row">
                    {contests.length == 0 && 
                    <h4>You don't have any contest active :(</h4>
                    }
                    {contests.map(h => 
                      {return <div className="card m-2" style={{width: "18rem"}}>
                        <img className="card-img-top img-fluid img-size" src={urlBanner+h.banner} alt={h.name}/>
                            <div className="card-body">
                                <h5 className="card-title">{h.name}</h5>
                                <Button className="m-1" variant="outline-danger" onClick={() => {
                                  setContestSelected(h);
                                  setShowDeleteModal(true);
                                }}>Delete</Button>
                                <Button className="m-1" variant="outline-info" onClick={() => {
                                  setContestSelected(h);
                                  setShowEditModal(true);
                                }}>Edit</Button>
                                <Button className="m-1" variant="outline-info" href={'/contest/' + h.url}>Details</Button>
                            </div>
                        </div>})}
        </div>  

        <Modal show={showCreateModal} idEvent={contestSelected} onHide={() => setShowCreateModal(false)}>
              <div className="modal-content">
                <div className="modal-header">
                  <h5 className="modal-title" id="addCreateContest">
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
                        id="inputBanner"
                        type="file"
                        className="form-control-file"
                        onChange={(e) => setBanner(e.target.files[0])}
                      />
                    </div>
                    <div className="form-group">
                      <label htmlfor="inputUrl">Url</label>
                      <input
                        id="inputUrl"
                        type="text"
                        className="form-control"
                        onChange={(e) => setUrl(e.target.value)}
                      />
                    </div>
                    <div className="form-group">
                      <label htmlfor="inputPrice">Begin Date</label>
                      <input
                      id="inputBeginDate"
                      type="date"
                      className="form-control"
                      onChange={date => setBegin_date(new Date(date.target.value))}
                      />
                    </div>
                    <div className="form-group">
                      <label htmlfor="inputPrice">End  Date</label>
                      <input
                      id="inputEndDate"
                      type="date"
                      className="form-control"
                      onChange={date => setEnd_date(new Date(date.target.value))}
                      />
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
                    Cancel
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
                  
            <Modal show={showEditModal} idEvent={contestSelected} onHide={() => setShowEditModal(false)}>
              <div className="modal-content">
                <div className="modal-header">
                  <h5 className="modal-title" id="addProductModalLabel">
                    Edit a Contest
              </h5>
                  <button
                    type="button"
                    className="close"
                    data-dismiss="modal"
                    aria-label="Close"
                    onClick={() => setShowEditModal(false)}
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
                        placeholder={contestSelected.name}
                        id="inputName"
                        onChange={(e) => setName(e.target.value)}
                      />
                    </div>
                    <div className="form-group">
                      <label htmlfor="inputType">Banner</label>
                      <input
                        type="file"
                        className="form-control-file"
                        onChange={(e) => setBanner(e.target.files[0])}
                      />
                    </div>
                    <div className="form-group">
                      <label htmlfor="inputQuantity">Url</label>
                      <input
                        type="text"
                        className="form-control"
                        placeholder={contestSelected.url}
                        onChange={(e) => setUrl(e.target.value)}
                      />
                    </div>
                    <div className="form-group">
                      <label htmlfor="inputPrice">Begin Date</label>
                      <input
                      id="inputBeginDate"
                      type="date"
                      className="form-control"
                      onChange={date => {setBegin_date(new Date(date.target.value))
                                        setDateChange(true)}}
                      />
                    </div>
                    <div className="form-group">
                      <label htmlfor="inputPrice">End  Date</label>
                      <input
                      id="inputEndDate"
                      type="date"
                      className="form-control"
                      onChange={date => {setEnd_date(new Date(date.target.value))
                                        setDateChange(true)}}
                      />
                    </div>
                    <div className="form-group">
                      <label htmlfor="inputPrice">Prize</label>
                      <input
                        type="number"
                        className="form-control"
                        placeholder={contestSelected.prize}
                        onChange={(e) => setPrize(e.target.value)}
                      />
                    </div>
                    <div className="form-group">
                      <label htmlfor="inputPrice">Script</label>
                      <input
                        type="text"
                        placeholder={contestSelected.script}
                        className="form-control"
                        onChange={(e) => setScript(e.target.value)}
                      />
                    </div>
                    <div className="form-group">
                      <label htmlfor="inputPrice">Recommendations</label>
                      <input
                        type="text"
                        className="form-control"
                        placeholder={contestSelected.recommendations}
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
                    onClick={() => setShowEditModal(false)}
                  >
                    Cancel
              </button>
                  <button
                    type="button"
                    className="btn btn-success"
                    onClick={() => editContest()}
                  >
                    Edit Constest
              </button>
                </div>
              </div>
            </Modal>
            
            <Modal show={showDeleteModal} onHide={() => setShowDeleteModal(false)}>
              <div className="modal-content">
                <div className="modal-header">
                    <h5 className="modal-title" id="addProductModalLabel">
                      Are you sure?
                    </h5>
                    <button
                        type="button"
                        className="close"
                        data-dismiss="modal"
                        aria-label="Close"
                        onClick={() => setShowDeleteModal(false)}
                    >
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div className="modal-footer">
                <button
                    type="button"
                    className="btn btn-info m-2"
                    data-dismiss="modal"
                    onClick={() => setShowDeleteModal(false)}
                  >
                    No
                  </button>
                  <button
                    type="button"
                    className="btn btn-danger m-2"
                    data-dismiss="modal"
                    onClick={() => deleteContest(contestSelected.url)}
                  >
                    Yes
                  </button>
                </div>
              </div>
            </Modal>
            <Snackbar open={errorModal} autoHideDuration={6000} onClose={handleClose}>
                <MuiAlert onClose={handleClose} severity="error">
                  {message}
                </MuiAlert>
            </Snackbar>
    </div>)
}