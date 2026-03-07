import { useState } from "react";
import { registerUser } from "../api/api";

export default function Register({ setPage }) {

  const [email,setEmail] = useState("");
  const [password,setPassword] = useState("");

  const handleRegister = async () => {

    try{

      await registerUser({
        email,
        password
      });

      alert("Registration successful. Please login.");

      setPage("login");

    }catch(err){

      console.error(err);
      alert("Registration failed");

    }

  };

  return(

    <div className="flex items-center justify-center h-screen bg-gray-100">

      <div className="bg-white p-8 rounded shadow w-96">

        <h1 className="text-xl font-bold mb-4">
          Register
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
          onClick={handleRegister}
          className="bg-green-600 text-white w-full p-2 rounded"
        >
          Register
        </button>

        <p
          className="mt-4 text-blue-600 cursor-pointer"
          onClick={()=>setPage("login")}
        >
          Already have an account? Login
        </p>

      </div>

    </div>
  );
}