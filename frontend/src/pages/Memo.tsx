import { useGetMemo } from "../utilities/myQuery";
import {
  IoIosTrash,
  IoIosEye,
  IoMdCreate,
} from "react-icons/io";

export function Memo() {
  const { data, isLoading, isError } = useGetMemo();

  return (
    <div>
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 py-4 px-6 ">
        {/* Title */}
        <h1 className="text-2xl sm:text-3xl font-bold text-slate-800">
          Memo
        </h1>

        {/* Search Bar */}

        <div className="flex items-center gap-2 bg-gray-100 rounded-full px-4 py-2 border border-gray-300 focus-within:ring-2 focus-within:ring-blue-500 transition">
          {/* <CiSearch className="text-gray-500" size={20} /> */}
          <input
            type="text"
            placeholder="Search Memo..."
            className="bg-transparent outline-none text-sm text-gray-700 w-40 sm:w-64"
            // value={searchInput}
            // onChange={(e) => setSearchInput(e.target.value)}
          />
        </div>
      </div>
      <div>
        <table className="min-w-full divide-y divide-slate-200 rounded-xl overflow-hidden shadow-lg bg-white">
          <thead className="bg-slate-100 text-slate-700 text-sm font-semibold tracking-wide">
            <tr>
              <th className="px-6 py-4 text-left">Nomor</th>
              <th className="px-6 py-4 text-left">Judul</th>
              <th className="px-6 py-4 text-left">PIC</th>
              <th className="px-6 py-4 text-left">Tanggal</th>
              <th className="px-6 py-4 text-center">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 text-sm text-slate-600">
            {data?.map((each, idx) => (
              <tr key={idx} className="hover:bg-slate-50 transition">
                <td className="px-6 py-4 font-medium text-slate-800">
                  {each.no_memo}
                </td>
                <td className="px-6 py-4">{each.judul_memo}</td>
                <td className="px-6 py-4">{each.penulis_memo}</td>
                <td className="px-6 py-4">{each.tanggal_buat}</td>
                <td className="px-6 py-4 flex justify-center gap-3 text-slate-500">
                  <button className="hover:text-indigo-600 transition">
                    <IoIosEye size={18} />
                  </button>
                  <button className="hover:text-green-600 transition">
                    <IoMdCreate size={18} />
                  </button>
                  <button className="hover:text-red-600 transition">
                    <IoIosTrash size={18} />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Hidden Pop up */}
    </div>
  );
}
