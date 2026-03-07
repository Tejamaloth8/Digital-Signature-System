import { useState } from "react";
import { loginUser } from "../api/api";

export default function Login({ setToken, setPage }) {

  const [email,setEmail] = useState("");
  const [password,setPassword] = useState("");

  const handleLogin = async () => {

    try{

      const res = await loginUser({
        email,
        password
      });

      localStorage.setItem("token",res.data.access_token);
      setToken(res.data.access_token);

    }catch(err){

      console.error(err);
      alert("Login failed");

    }
  }

  return(

    <div className="flex items-center justify-center h-screen bg-gray-100">

      <div className="bg-white p-8 rounded shadow w-96">

        <h1 className="text-xl font-bold mb-4">
          Digital Signature Login
        </h1>

        <input
          placeholder="Email"
          className="border w-full p-2 mb-3"
          onChange={(e)=>setEmail(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          className="border w-full p-2 mb-3"
          onChange={(e)=>setPassword(e.target.value)}
        />

        <button
          onClick={handleLogin}
          className="bg-blue-600 text-white w-full p-2 rounded"
        >
          Login
        </button>

        <p
          className="mt-4 text-blue-600 cursor-pointer text-center"
          onClick={()=>setPage("register")}
        >
          Create new account
        </p>

      </div>

    </div>
  )
}