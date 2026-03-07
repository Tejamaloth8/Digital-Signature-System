import axios from "axios";

const API = axios.create({
  baseURL: "https://digital-signature-system.onrender.com"
});

export const registerUser = (data) =>
  API.post("/register", data);

export const loginUser = (data) =>
  API.post("/login",data);

export const uploadFile = (formData,token) =>
  API.post("/upload",formData,{
    headers:{
      Authorization:`Bearer ${token}`,
      "Content-Type":"multipart/form-data"
    }
  });

export const signDocument = (id,token) =>
  API.post(`/sign/${id}`,{},{
    headers:{
      Authorization:`Bearer ${token}`
    }
  });

export const verifyDocument = (id)=>
  API.get(`/verify/${id}`);