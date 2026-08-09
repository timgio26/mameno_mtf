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
<div className="min-h-screen bg-slate-50 text-slate-800 font-sans">
  {/* Sidebar */}
  <aside className="fixed inset-y-0 left-0 z-30 flex w-72 flex-col border-r border-slate-200 bg-white shadow-sm">
    {/* Logo / Header */}
    <div className="flex h-20 shrink-0 items-center gap-3 border-b border-slate-200 px-6">
      <img
        src={logo}
        alt="Logo"
        className="h-11 w-11 rounded-xl object-cover shadow-sm"
      />

      <div>
        <h1 className="text-xl font-bold tracking-tight text-slate-800">
          AR APP
        </h1>
        <p className="text-xs text-slate-400">
          AR MTF
        </p>
      </div>
    </div>

    {/* Navigation */}
    <nav className="flex-1 overflow-y-auto px-4 py-6">
      <p className="mb-3 px-3 text-xs font-semibold uppercase tracking-wider text-slate-400">
        Menu
      </p>

      <div className="space-y-1">
        <NavLink
          to="/"
          className={({ isActive }) =>
            `flex items-center rounded-lg px-3 py-2.5 text-sm font-medium transition-all ${
              isActive
                ? "bg-blue-50 text-blue-600 shadow-sm"
                : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
            }`
          }
        >
          Nota
        </NavLink>

        <NavLink
          to="/memo"
          className={({ isActive }) =>
            `flex items-center rounded-lg px-3 py-2.5 text-sm font-medium transition-all ${
              isActive
                ? "bg-blue-50 text-blue-600 shadow-sm"
                : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
            }`
          }
        >
          Memo
        </NavLink>

        <NavLink
          to="/pembelian"
          className={({ isActive }) =>
            `flex items-center rounded-lg px-3 py-2.5 text-sm font-medium transition-all ${
              isActive
                ? "bg-blue-50 text-blue-600 shadow-sm"
                : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
            }`
          }
        >
          Form Pembelian
        </NavLink>

        <NavLink
          to="/bersama"
          className={({ isActive }) =>
            `flex items-center rounded-lg px-3 py-2.5 text-sm font-medium transition-all ${
              isActive
                ? "bg-blue-50 text-blue-600 shadow-sm"
                : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
            }`
          }
        >
          Nota Bersama
        </NavLink>

        {userData?.role === "admin" && (
          <NavLink
            to="/user"
            className={({ isActive }) =>
              `flex items-center rounded-lg px-3 py-2.5 text-sm font-medium transition-all ${
                isActive
                  ? "bg-blue-50 text-blue-600 shadow-sm"
                  : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
              }`
            }
          >
            User
          </NavLink>
        )}

        {/* Download */}
        <button
          type="button"
          onClick={handle_download}
          disabled={downloading}
          className="flex w-full items-center rounded-lg px-3 py-2.5 text-left text-sm font-medium text-slate-600 transition-all hover:bg-slate-50 hover:text-slate-900 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {downloading ? "Loading..." : "Download"}
        </button>
      </div>
    </nav>

    {/* Bottom Section */}
    <div className="shrink-0 border-t border-slate-200">
      {/* Logout */}
      <button
        type="button"
        onClick={()=>{logout()}}
        className="mx-4 my-4 flex w-[calc(100%-2rem)] items-center rounded-lg px-3 py-2.5 text-left text-sm font-medium text-slate-600 transition-all hover:bg-red-50 hover:text-red-600"
      >
        Logout
      </button>

      {/* Footer */}
      <div className="border-t border-slate-100 px-6 py-4">
        <p className="text-xs font-medium text-slate-500">
          &copy; {year} AR MTF
        </p>

        <p className="mt-1 text-xs italic text-slate-400">
          Crafted with care in Indonesia
        </p>
      </div>
    </div>
  </aside>

  {/* Main Content */}
  <div className="ml-72 min-h-screen">
    <main className="min-h-screen px-6 py-8 lg:px-10">
      <div className="mx-auto max-w-7xl">
        <Outlet />
      </div>
    </main>
  </div>

  {/* Floating Action Button */}
  <button
    onClick={() => setShowModal(true)}
    className="fixed bottom-6 right-6 z-40 flex h-14 w-14 items-center justify-center rounded-full bg-blue-600 text-white shadow-lg shadow-blue-600/30 transition-all hover:scale-105 hover:bg-blue-700 active:scale-95"
    aria-label="Open modal"
  >
    <FaPlus className="text-lg" />
  </button>

  {/* Hidden Pop Up */}
  <PopupModal
    visible={showModal}
    children={
      <NewForm setShowModal={setShowModal} />
    }
  />
</div>


  );
}