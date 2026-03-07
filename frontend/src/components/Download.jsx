import { useState } from "react";
import { downloadDocument } from "../api/api";

export default function Download({token}){

  const [docId,setDocId] = useState("");

  const handleDownload = async ()=>{

    try{

      const res = await downloadDocument(docId,token);

      const url = window.URL.createObjectURL(
        new Blob([res.data])
      );

      const link = document.createElement("a");

      link.href = url;
      link.setAttribute("download","document");

      document.body.appendChild(link);
      link.click();

    }catch(err){

      console.error(err);
      alert("Download failed");

    }

  };

  return(

    <div>

      <h2 className="text-xl font-bold mb-4">
        Download Document
      </h2>

      <input
        placeholder="Document ID"
        className="border p-2 mr-2"
        onChange={(e)=>setDocId(e.target.value)}
      />

      <button
        onClick={handleDownload}
        className="bg-blue-700 text-white px-4 py-2 rounded"
      >
        Download
      </button>

    </div>

  )
}