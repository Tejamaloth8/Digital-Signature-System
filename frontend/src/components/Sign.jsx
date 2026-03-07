import { useState } from "react";
import { signDocument } from "../api/api";

export default function Sign({ token }) {

  const [docId,setDocId] = useState("");

  const handleSign = async () => {

    try{

      await signDocument(docId,token);

      alert("Document signed successfully");

    }catch(err){

      console.error(err);
      alert("Sign failed");

    }

  };

  return(

    <div>

      <h2 className="text-xl font-bold mb-4">
        Sign Document
      </h2>

      <input
        placeholder="Document ID"
        className="border p-2"
        onChange={(e)=>setDocId(e.target.value)}
      />

      <button
        onClick={handleSign}
        className="ml-3 bg-purple-600 text-white px-4 py-2 rounded"
      >
        Sign
      </button>

    </div>
  );
}