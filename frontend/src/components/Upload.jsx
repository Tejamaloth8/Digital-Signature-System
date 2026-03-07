import { useState } from "react";
import { uploadFile } from "../api/api";

export default function Upload({ token }) {

  const [file,setFile] = useState(null);
  const [message,setMessage] = useState("");

  const handleUpload = async () => {

    if(!file){
      alert("Select file first");
      return;
    }

    const formData = new FormData();
    formData.append("file",file);

    try{

      const res = await uploadFile(formData,token);

      setMessage("Uploaded successfully. Document ID: "+res.data.document_id);

    }catch(err){
      console.error(err);
      alert("Upload failed");
    }
  };

  return(

    <div>

      <h2 className="text-xl font-bold mb-4">
        Upload Document
      </h2>

      <input
        type="file"
        onChange={(e)=>setFile(e.target.files[0])}
      />

      <button
        onClick={handleUpload}
        className="ml-3 bg-blue-600 text-white px-4 py-2 rounded"
      >
        Upload
      </button>

      {message && (
        <p className="mt-3 text-green-600">
          {message}
        </p>
      )}

    </div>
  );
}