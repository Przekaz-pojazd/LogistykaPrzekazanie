import axios from "axios";
import React, { useState, useEffect } from "react";


const client = axios.create({
    baseURL: "http://127.0.0.1:8000/"
});

client.defaults.xsrfCookieName = 'csrftoken';
client.defaults.xsrfHeaderName = 'X-CSRFToken';
client.defaults.withCredentials = true;
const endpoint = '/api/vehicle-receivements/complain/semitruck/add';
function SemiTrailerPhoto(){
    const [photo, setPhoto] = useState(null);

    let handlePhoto = (e) =>{
        setPhoto(e.target.files[0]);
    }

    let handleSubmit = async(e) => {
        e.preventDefault();
        let data = new FormData();
        data.append('semitrailer_photo', photo);
        try{
            const response = await client.post(endpoint, data,{
                headers: {
                    "Content-Type": "multipart/form-data",
                }
            });
            console.log("Wysłano zdjecie");
            console.log(response);
        }catch (error){
            console.log(error);
        }
    }
    return (
        <div>
            <h1>Upload SemitruckPhoto</h1>
            <input type="file" onChange={handlePhoto}/>
            <button type="submit" onClick={handleSubmit}>Upload</button>
        </div>
    )
}

export default SemiTrailerPhoto;