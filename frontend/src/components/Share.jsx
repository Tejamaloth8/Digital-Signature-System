import { useState } from "react";
import { shareDocument } from "../api/api";

export default function Share({ token }){

  const [docId,setDocId] = useState("");
  const [email,setEmail] = useState("");

  const handleShare = async ()=>{

    try{

      await shareDocument(docId,email,token);

      alert("Document shared successfully");

    }catch(err){

      console.error(err);
      alert("Share failed");

    }

  };

  return(

    <div>

      <h2 className="text-xl font-bold mb-4">
        Share Document
      </h2>

      <input
        placeholder="Document ID"
        className="border p-2 mr-2"
        onChange={(e)=>setDocId(e.target.value)}
      />

      <input
        placeholder="Recipient Email"
        className="border p-2 mr-2"
        onChange={(e)=>setEmail(e.target.value)}
      />

      <button
        onClick={handleShare}
        className="bg-orange-600 text-white px-4 py-2 rounded"
      >
        Share
      </button>

    </div>

  )
}