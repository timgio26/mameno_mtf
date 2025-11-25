import { useEffect, useState } from "react";
import { useAddData, type IAddDataResp } from "../utilities/myQuery";

type NewFormProp = {
  setShowModal :React.Dispatch<React.SetStateAction<boolean>>
}

export function NewForm({setShowModal}:NewFormProp) {
  const [judul, setJudul] = useState<string>();
  const [kategori, setKategori] = useState<string>();
  const [divisi, setDivisi] = useState<string>();
  const [divisiList, setDivisiList] = useState<string[]>([]);
  const {data,mutate,isPending} = useAddData(kategori)
  const [result,setResult] = useState<IAddDataResp|undefined>()

  useEffect(()=>{
    setResult(data)
  },[data])

  function addDivisi() {
    if (!divisi) return;
    if (divisiList.includes(divisi.toUpperCase()))return;
    setDivisiList((curstate) => [...curstate, divisi.toUpperCase()]);
    setDivisi("")
  }

  function removeDivisi(idx:number){
    setDivisiList((curstate)=>(curstate.filter((_,index)=>index!=idx)));
  }

  function submitForm(){
    // console.log("submit")
    if(!judul||!kategori)return;
    // console.log("mutate")
    mutate({judul,divisi:divisiList})
  }

  return (
    <div className="space-y-3 max-h-[80vh] overflow-y-auto">
      {data ? (
        <>
          {/* Header */}
          <div>
            <h2 className="text-2xl font-bold text-slate-800">📝 New Nota</h2>
          </div>
<div className="space-y-2">
  <p className="text-slate-700">
    <span className="font-semibold">Judul:</span> {data.judul}
  </p>
  <p className="text-slate-700">
    <span className="font-semibold">No. Document:</span> {data.no_doc}
  </p>
  <p className="text-slate-700">
    <span className="font-semibold">PIC:</span> {data.pic}
  </p>
</div>

        </>
      ) : (
        <>
          {/* Header */}
          <div>
            <h2 className="text-2xl font-bold text-slate-800">📝 New Nota</h2>
            <p className="text-sm text-slate-500 mt-1">
              Fill in the details below to create a new nota or memo.
            </p>
          </div>

          {/* Judul */}
          <div className="flex flex-col gap-2">
            <label
              htmlFor="Judul"
              className="text-sm font-semibold text-slate-700"
            >
              Judul Nota/Memo
            </label>
            <textarea
              name="Judul"
              id="Judul"
              rows={2}
              className="rounded-lg border border-slate-300 px-4 py-2 text-sm shadow-sm resize-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition"
              value={judul}
              onChange={(e) => setJudul(e.target.value)}
            />
          </div>

          {/* Kategori */}
          <div className="flex flex-col gap-2">
            <label
              htmlFor="Kategori"
              className="text-sm font-semibold text-slate-700"
            >
              Kategori
            </label>
            <select
              name="Kategori"
              id="Kategori"
              className="rounded-lg border border-slate-300 px-4 py-2 text-sm shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition"
              value={kategori}
              onChange={(e) => setKategori(e.target.value)}
            >
              <option value="" hidden>
                Select category
              </option>
              <option value="nota">Nota</option>
              <option value="memo">Memo</option>
              <option value="pembelian">Form Pembelian</option>
              <option value="bersama">Nota Bersama</option>
            </select>
          </div>

          {/* Divisi List */}
          {kategori == "bersama" && (
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
                  value={divisi}
                  onChange={(e) => setDivisi(e.target.value)}
                />
                <button
                  type="button"
                  onClick={addDivisi}
                  className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition font-semibold text-sm"
                >
                  + Add
                </button>
              </div>
            </div>
          )}

          {/* DocUrl */}
          {/* <div className="flex flex-col gap-2">
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
              // value={judul}
              // onChange={(e) => setJudul(e.target.value)}
            />
          </div> */}
        </>
      )}

      {/* Actions */}
      <div className="pt-4 flex justify-end gap-4 border-t border-slate-200">
        <button
          className="px-4 py-2 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium transition"
          onClick={() => setShowModal(false)}
        >
          {result ? "Close" : "Cancel"}
        </button>
        {!result && (
          <button
            className="px-4 py-2 rounded-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold transition"
            onClick={submitForm}
          >
            {isPending ? "Loading..." : "Submit"}
          </button>
        )}
      </div>
    </div>
  );
}
