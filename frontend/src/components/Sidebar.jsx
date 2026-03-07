import { FaUpload,FaSignature,FaCheckCircle } from "react-icons/fa";

export default function Sidebar({setPage}){

  return(
    <div className="w-64 bg-slate-900 text-white min-h-screen p-6">

      <h1 className="text-xl font-bold mb-8">
        Digital Signature
      </h1>

      <div className="flex flex-col gap-4">

        <button onClick={()=>setPage("upload")} className="hover:bg-slate-700 p-2 rounded flex gap-2">
          <FaUpload/> Upload
        </button>

        <button onClick={()=>setPage("sign")} className="hover:bg-slate-700 p-2 rounded flex gap-2">
          <FaSignature/> Sign
        </button>

        <button onClick={()=>setPage("verify")} className="hover:bg-slate-700 p-2 rounded flex gap-2">
          <FaCheckCircle/> Verify
        </button>

      </div>

    </div>
  )
}