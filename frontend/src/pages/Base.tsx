import { NavLink, Outlet } from "react-router";
import logo from "../assets/logo.png";
import { FaPlus } from "react-icons/fa";
import { useState } from "react";
import { PopupModal } from "../components/PopUpModal";
import { NewForm } from "../components/NewForm";
import { downloadData, useLogOut, useUserCheck } from "../utilities/myQuery";


export function Base() {
  const year = new Date().getFullYear();
  const {mutate:logout} = useLogOut()
  const [showModal,setShowModal] = useState<boolean>(false)
  const [downloading,setIsDownloading] = useState<boolean>(false) 
  const { data:userData } = useUserCheck();

  async function handle_download(){
    setIsDownloading(true)
    await downloadData()
    setIsDownloading(false)
  }
  

  return (
    <div className="min-h-screen flex from-slate-50 to-slate-100 text-gray-800 font-sans">
      {/* Sidebar */}
      <aside className="w-72 bg-white shadow-xl border-r border-slate-200 flex flex-col justify-between">
        {/* Top Section */}
        <div>
          <div className="flex items-center gap-3 p-6 border-b border-slate-200">
            <img
              src={logo}
              alt="Logo"
              className="h-12 w-12 rounded-lg shadow-md"
            />
            <h1 className="text-3xl font-bold tracking-tight text-slate-800">
              AR APP
            </h1>
          </div>

          <nav className="flex flex-col p-6 gap-3">
            <NavLink to="/" className={({isActive})=>isActive?"text-base font-medium text-blue-600":"text-base font-medium"}>Nota</NavLink>
            <NavLink to="/memo" className={({isActive})=>isActive?"text-base font-medium text-blue-600":"text-base font-medium"}>Memo</NavLink>
            <NavLink to="/pembelian" className={({isActive})=>isActive?"text-base font-medium text-blue-600":"text-base font-medium"}>Form Pembelian</NavLink>
            <NavLink to="/bersama" className={({isActive})=>isActive?"text-base font-medium text-blue-600":"text-base font-medium"}>Nota Bersama</NavLink>
            {userData?.role=='admin'&&
            <NavLink to="/user" className={({isActive})=>isActive?"text-base font-medium text-blue-600":"text-base font-medium"}>User</NavLink>
            }
            <span className="text-base font-medium cursor-pointer" onClick={handle_download}>{downloading?"Loading...":"Download"}</span>

          </nav>

        </div>

        <div>

        <div className="p-6 ">
              
            <span className="text-base font-medium flex cursor-pointer" onClick={()=>{logout()}}>Logout</span>
            </div>

        {/* Bottom Section */}
        <div className="p-6 border-t border-slate-200">
          
          <div className="text-sm text-slate-500 leading-relaxed">
            <p className="font-medium tracking-wide">&copy; {year} AR MTF</p>
            <p className="italic text-slate-400">
              Crafted with care in Indonesia
            </p>
          </div>
        </div>
        </div>
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        <main className="flex-1 overflow-y-auto px-6 py-10">
          <div className="max-w-6xl mx-auto">
            <Outlet />
          </div>
        </main>
      </div>

      <button
        onClick={() => setShowModal(true)}
        className="fixed bottom-5 right-6 z-40 bg-blue-600 text-white p-4 rounded-full shadow-lg hover:opacity-80 transition-opacity"
        aria-label="Open modal"
      >
        <FaPlus />
      </button>

      {/* Hidden Pop Up */}
      <PopupModal visible={showModal} children={<NewForm setShowModal={setShowModal}/>}/>
    </div>
  );
}