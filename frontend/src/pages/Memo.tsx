import {  useState } from "react";
import { PopupModal } from "../components/PopUpModal";
import { useDelMemo, useGetMemo, useUserCheck, type IMemo } from "../utilities/myQuery";
import {
  IoIosTrash,
  // IoIosEye,
  IoMdCreate,
  IoIosCloseCircleOutline,
} from "react-icons/io";
import { Loading } from "../components/Loading";
import { Error } from "../components/Error";
import { EditFormMemo } from "../components/EditFormMemo";
import { Pagination } from "../components/Pagination";
import { InputWithLimiter } from "../components/InputWithLimiter";

export function Memo() {
  const [page,setPage] = useState<number>(1)
  const [search, setSearch] = useState<string>("");
  // const [searchInput, setSearchInput] = useState<string>("");
  const { data, isLoading, isError } = useGetMemo(page,search);
  const [showDelPopup, setShowDelPopup] = useState<boolean>(false);
  const [selectedData, setSelectedData] = useState<IMemo>();
  const { mutate: delete_memo, isPending: is_deleting } = useDelMemo();
  const [showEditPopup, setShowEditPopup] = useState<boolean>(false);
  const { data:userData } = useUserCheck();



  function handleDeleteMemo() {
    if (!selectedData) return;
    delete_memo(selectedData.id, {
      onSuccess: () => {
        setSelectedData(undefined);
        setShowDelPopup(false);
      },
    });
  }

  if (isLoading) {
    return <Loading />;
  }

  if (isError||!userData) {
    return <Error />;
  }

  return (
    <div>
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 py-4 px-6 ">
        {/* Title */}
        <h1 className="text-2xl sm:text-3xl font-bold text-slate-800">Memo</h1>

        {/* Search Bar */}

        <div className="flex items-center gap-2 bg-gray-100 rounded-full px-4 py-2 border border-gray-300 focus-within:ring-2 focus-within:ring-blue-500 transition">

          <InputWithLimiter
            placeholder="Search Nota..."
            functionAfterDelay={(val:string) => {
              setPage(1);
              setSearch(val);
            }}
          />
        </div>
      </div>
      {data && data.data.length > 0 ? (
        <div>
          <table className="min-w-full divide-y divide-slate-200 rounded-xl overflow-hidden shadow-lg bg-white">
            <thead className="bg-slate-100 text-slate-700 text-sm font-semibold tracking-wide">
              <tr>
                <th className="px-6 py-4 text-left">Nomor</th>
                <th className="px-6 py-4 text-left">Judul</th>
                <th className="px-6 py-4 text-left">PIC</th>
                <th className="px-6 py-4 text-left">Tanggal</th>
                {userData.role=='admin'&&
                <th className="px-6 py-4 text-center">Actions</th>
                }
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-sm text-slate-600">
              {data.data.map((each, idx) => (
                <tr key={idx} className="hover:bg-slate-50 transition">
                  <td className="px-6 py-4 font-medium text-slate-800">
                    {each.no_memo}
                  </td>
                  <td className="px-6 py-4">{each.judul_memo}</td>
                  <td className="px-6 py-4">{each.penulis_memo}</td>
                  <td className="px-6 py-4">{each.tanggal_buat.split("00")[0].trim()}</td>
                  {userData.role=='admin'&&
                  <td className="px-6 py-4 flex justify-center gap-3 text-slate-500">
                    {/* <button className="hover:text-indigo-600 transition">
                    <IoIosEye size={18} />
                  </button> */}
                    <button
                      className="hover:text-green-600 transition"
                      onClick={() => {
                        setSelectedData(each);
                        setShowEditPopup(true);
                      }}
                    >
                      <IoMdCreate size={18} />
                    </button>
                    <button
                      className="hover:text-red-600 transition"
                      onClick={() => {
                        setSelectedData(each);
                        setShowDelPopup(true);
                      }}
                    >
                      <IoIosTrash size={18} />
                    </button>
                  </td>
                  }
                </tr>
              ))}
            </tbody>
          </table>
          <Pagination onNext={()=>{setPage((curPage)=>curPage+1)}} onPrev={()=>{setPage((curPage)=>curPage-1)}} page={page} total_page={data.total_pages}/>
        </div>
      ) : (
        <div className="flex flex-col items-center justify-center text-center text-gray-500 py-12">
          <p className="text-lg font-medium">No data found.</p>
          <p className="text-sm mt-1">Start by adding a new data below.</p>
        </div>
      )}

      {/* Hidden Pop up */}
      <PopupModal visible={showDelPopup}>
        {/* Content Slot */}
        <div className="space-y-4">
          <p className="text-sm text-gray-700">
            Are you sure you want to delete{" "}
            {/* <strong>{selectedUser.name}</strong>? */}
          </p>
        </div>
        {/* Icon */}
        <div className="flex justify-center mt-6">
          <IoIosCloseCircleOutline size={64} className="text-red-500" />
        </div>
        {/* Button */}
        <div className="mt-6 flex justify-end gap-3">
          <button
            onClick={() => setShowDelPopup(false)}
            className="px-4 py-2 rounded-full bg-gray-100 hover:bg-gray-200 text-sm font-medium text-gray-700 transition"
          >
            Cancel
          </button>
          <button
            onClick={handleDeleteMemo}
            data-testid="confirmButton"
            className="px-4 py-2 rounded-full bg-red-600 hover:bg-red-700 text-sm font-medium text-white transition"
          >
            {is_deleting ? "Loading" : "Delete"}
            {/* Delete */}
          </button>
        </div>
      </PopupModal>

      {selectedData && (
        <PopupModal
          visible={showEditPopup}
          children={
            <EditFormMemo setShowModal={setShowEditPopup} data={selectedData} />
          }
        />
      )}
    </div>
  );
}
