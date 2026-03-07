import { useState } from "react";
import { verifyDocument } from "../api/api";

export default function Verify() {

  const [docId,setDocId] = useState("");
  const [result,setResult] = useState(null);

  const handleVerify = async () => {

    try{

      const res = await verifyDocument(docId);

      setResult(res.data);

    }catch(err){

      console.error(err);
      alert("Verification failed");

    }

  };

  return(

    <div>

      <h2 className="text-xl font-bold mb-4">
        Verify Document
      </h2>

      <input
        placeholder="Document ID"
        className="border p-2"
        onChange={(e)=>setDocId(e.target.value)}
      />

      <button
        onClick={handleVerify}
        className="ml-3 bg-green-600 text-white px-4 py-2 rounded"
      >
        Verify
      </button>

      {result && (

        <div className="mt-4">

          <p>Ed25519 Valid: {result.ed25519_valid.toString()}</p>
          <p>Heisenberg Valid: {result.heisenberg_valid.toString()}</p>

        </div>

      )}

    </div>
  );
}