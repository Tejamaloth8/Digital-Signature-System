import { useState } from "react";
import Sidebar from "../components/Sidebar";
import Upload from "../components/Upload";
import Sign from "../components/Sign";
import Verify from "../components/Verify";
import Share from "../components/Share";
import Download from "../components/Download";

export default function Dashboard({ token }) {

  const [page,setPage] = useState("upload");

  const renderPage = () => {

    if(page === "upload") return <Upload token={token}/>
    if(page === "sign") return <Sign token={token}/>
    if(page === "verify") return <Verify token={token}/>
    if(page === "share") return <Share token={token}/>
    if(page === "download") return <Download token={token}/>
  }

  return(

    <div className="flex">

      <Sidebar setPage={setPage}/>

      <div className="flex-1 bg-slate-100 p-8">

        {renderPage()}

      </div>

    </div>
  )
}