import { useState } from "react";
import { useUpdateBersama, type IBersama } from "../utilities/myQuery"

type EditFormProp = {
  setShowModal :React.Dispatch<React.SetStateAction<boolean>>;
  data :IBersama
}

export function EditFormBersama({setShowModal,data}:EditFormProp){
    const [judulEdit,setJudulEdit] = useState<string>(data.judul) 
    const [urlEdit,setUrlEdit] =useState<string|null>(data.link)
    const {mutate,isPending} = useUpdateBersama()

    function submitForm(){
      mutate({id:data.id,judul:judulEdit,url:urlEdit},{
        onSuccess:()=>{
          setShowModal(false)
        }
      })
    }
    return(
        <div className="space-y-3 max-h-[80vh] overflow-y-auto">
        <>
          {/* Header */}
          <div>
            <h2 className="text-2xl font-bold text-slate-800">📝 Edit Form Pembelian</h2>
            {/* <p className="text-sm text-slate-500 mt-1">
              Fill in the details below to create a new nota or memo.
            </p> */}
          </div>

        {/* NO Doc */}
          <div className="flex flex-col gap-2">
            
            <span

              className="text-sm font-semibold text-slate-700"
            >
                No Form Pembelian
            </span>
            <span
              className="rounded-lg  border-slate-300 px-4 py-1 text-sm  resize-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition"
              >
                {data.no_bersama}
              </span>
          </div>

          {/* PIC */}
          <div className="flex flex-col gap-2">
            <span
              className="text-sm font-semibold text-slate-700"
            >
                PIC
            </span>
            <span
              className="rounded-lg  border-slate-300 px-4 py-1 text-sm  resize-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition"
              >
                {data.penulis}
              </span>
          </div>

          <div className="flex flex-col gap-2">
            <span
              className="text-sm font-semibold text-slate-700"
            >
                Tanggal
            </span>
            <span
              className="rounded-lg  border-slate-300 px-4 py-1 text-sm  resize-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition"
              >
                {data.tanggal_buat}
              </span>
          </div>

          {/* Judul */}
          <div className="flex flex-col gap-2">
            
            <label
              htmlFor="Judul"
              className="text-sm font-semibold text-slate-700"
            >
              Judul Form Pembelian
            </label>
            <textarea
              name="Judul"
              id="Judul"
              rows={2}
              className="rounded-lg border border-slate-300 px-4 py-2 text-sm shadow-sm resize-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition"
              value={judulEdit}
              onChange={(e) => setJudulEdit(e.target.value)}
            />
          </div>


          {/* Divisi List */}
          {/* {kategori == "bersama" && (
            <div
              className={`flex flex-col ${
                divisiList.length > 0 ? "gap-2" : "gap-1"
              }`}
            >
              <label
                htmlFor="divisi"
                className="text-sm font-semibold text-slate-700"
              >
                Kode Divisi
              </label>

              <div className="space-y-1">
                {divisiList.map((each, index) => (
                  <div
                    key={index}
                    className="flex justify-between items-center bg-slate-50 px-4 py-2 rounded-md border border-slate-200"
                  >
                    <span className="text-sm font-medium text-slate-700">
                      {each}
                    </span>
                    <button
                      type="button"
                      className="text-red-500 hover:text-red-700 font-bold cursor-pointer"
                      onClick={() => removeDivisi(index)}
                    >
                      ✕
                    </button>
                  </div>
                ))}
              </div>

              <div className="flex gap-3">
                <input
                  type="text"
                  name="divisi"
                  id="divisi"
                  className="flex-1 rounded-lg border border-slate-300 px-4 py-2 text-sm shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition"
                //   value={divisi}
                //   onChange={(e) => setDivisi(e.target.value)}
                />
                <button
                  type="button"
                //   onClick={addDivisi}
                  className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition font-semibold text-sm"
                >
                  + Add
                </button>
              </div>
            </div>
          )} */}

          {/* DocUrl */}
          <div className="flex flex-col gap-2">
            <label
              htmlFor="url"
              className="text-sm font-semibold text-slate-700"
            >
              Link to Document
            </label>
            <textarea
            placeholder="Enter a valid URL (e.g., https://example.com)"
              name="url"
              id="url"
              rows={2}
              className="rounded-lg border border-slate-300 px-4 py-2 text-sm shadow-sm resize-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition"
              value={urlEdit??undefined}
              onChange={(e) => setUrlEdit(e.target.value)}
            />
          </div>
        </>


      {/* Actions */}
      <div className="pt-4 flex justify-end gap-4 border-t border-slate-200">
        <button
          className="px-4 py-2 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium transition"
          onClick={() => setShowModal(false)}
        >
          {/* {result ? "Close" : "Cancel"} */}
          Cancel
        </button>

          <button
            className="px-4 py-2 rounded-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold transition"
            onClick={submitForm}
          >
            {/* Update */}
            {isPending ? "Loading..." : "Submit"}
          </button>
      </div>
    </div>
    )
}