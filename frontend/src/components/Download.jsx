import { useState } from "react";
import { downloadDocument } from "../api/api";

export default function Download({ token }) {

  const [docId,setDocId] = useState("");

  const handleDownload = async () => {

    try{

      const res = await downloadDocument(docId, token);

      const blob = new Blob([res.data], {
        type: res.headers["content-type"]
      });

      const url = window.URL.createObjectURL(blob);

      const link = document.createElement("a");
      link.href = url;

      let fileName = `document_${docId}`;

      const contentDisposition = res.headers["content-disposition"];

      if (contentDisposition) {
        const parts = contentDisposition.split("filename=");
        if (parts.length > 1) {
          fileName = parts[1].replace(/[";]/g, "").trim();
        }
      }

      link.download = fileName;

      document.body.appendChild(link);
      link.click();

      window.URL.revokeObjectURL(url);

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