import {
  IoIosCloseCircleOutline,
  IoIosTrash,
  IoMdCreate,
} from "react-icons/io";
import { Error } from "../components/Error";
import { Loading } from "../components/Loading";
import { useDelUser, useGetUser, type IUser } from "../utilities/myQuery";
import { PopupModal } from "../components/PopUpModal";
import { useEffect, useState } from "react";
import { NewUserForm } from "../components/NewUserForm";
import { EditUserForm } from "../components/EditUserForm";
import { Pagination } from "../components/Pagination";

export function User() {
  const [page,setPage] = useState<number>(1)
  const { data, isError, isLoading } = useGetUser(page);
  const { mutate, isPending: isDeleting } = useDelUser();
  const [addUserModalVisible, setAddUserModalVisible] =useState<boolean>(false);
  const [editUserModalVisible, setEditUserModalVisible] =useState<boolean>(false);
  const [delUserModalVisible, setDelUserModalVisible] =useState<boolean>(false);
  const [selectedData, setSelectedData] = useState<IUser>();

  useEffect(() => {
    if (!data || data.total_pages==0) return;
    if (page > data.total_pages) {
      setPage(data.total_pages);
    }
  }, [data]);

  function handleDelete() {
    if (!selectedData) return;
    mutate(selectedData.id, {
      onSuccess: () => {
        setDelUserModalVisible(false);
      },
    });
  }

  if (isLoading) {
    return <Loading />;
  }

  if (isError) {
    return <Error />;
  }
  return (
    <div>
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 py-4 px-6 ">
        {/* Title */}
        <h1 className="text-2xl sm:text-3xl font-bold text-slate-800">User</h1>

        {/* Search Bar */}

        <div
          className="flex items-center gap-2 bg-gray-100 rounded-full px-4 py-2 border border-gray-300 cursor-pointer hover:opacity-75"
          onClick={() => setAddUserModalVisible(true)}
        >
          {/* <div> */}
          <span>Add New User</span>
          {/* </div> */}
        </div>
      </div>
      {data ? (
        <div className="max-h-100 overflow-y-scroll">
          <table className="min-w-full divide-y divide-slate-200 rounded-xl overflow-hidden shadow-lg bg-white">
            <thead className="bg-slate-100 text-slate-700 text-sm font-semibold tracking-wide">
              <tr>
                <th className="px-6 py-4 text-left">Nama</th>
                <th className="px-6 py-4 text-left">Username</th>
                <th className="px-6 py-4 text-left">Role</th>
                <th className="px-6 py-4 text-left">Status</th>

                <th className="px-6 py-4 text-center">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-sm text-slate-600">
              {data.data.map((each, idx) => (
                <tr key={idx} className="hover:bg-slate-50 transition">
                  <td className="px-6 py-4 font-medium text-slate-800">
                    {each.nama}
                  </td>
                  <td className="px-6 py-4">{each.username}</td>
                  <td className="px-6 py-4">{each.role}</td>
                  <td className="px-6 py-4">{each.active==true?"Active":"Inactive"}</td>

                  <td className="px-6 py-4 flex justify-center gap-3 text-slate-500">
                    {/* <button className="hover:text-indigo-600 transition">
                                                <IoIosEye size={18} />
                                              </button> */}
                    <button
                      className="hover:text-green-600 transition"
                      onClick={() => {
                            setSelectedData(each);
                            setEditUserModalVisible(true)
                      }}
                    >
                      <IoMdCreate size={18} />
                    </button>
                    <button
                      className="hover:text-red-600 transition"
                      onClick={() => {
                        setSelectedData(each);
                        setDelUserModalVisible(true);
                      }}
                    >
                      <IoIosTrash size={18} />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
                    <Pagination
                      onNext={() => {
                        setPage((curPage) => curPage + 1);
                      }}
                      onPrev={() => {
                        setPage((curPage) => curPage - 1);
                      }}
                      page={page}
                      total_page={data.total_pages}
                    />
        </div>
      ) : (
        <div className="flex flex-col items-center justify-center text-center text-gray-500 py-12">
          <p className="text-lg font-medium">No data found.</p>
          <p className="text-sm mt-1">Start by adding a new data.</p>
        </div>
      )}

      <PopupModal
        visible={addUserModalVisible}
        children={<NewUserForm setShowModal={setAddUserModalVisible} />}
      />
      <PopupModal visible={delUserModalVisible}>
        <>
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
            onClick={() => setDelUserModalVisible(false)}
            className="px-4 py-2 rounded-full bg-gray-100 hover:bg-gray-200 text-sm font-medium text-gray-700 transition"
          >
            Cancel
          </button>
          <button
            onClick={handleDelete}
            data-testid="confirmButton"
            className="px-4 py-2 rounded-full bg-red-600 hover:bg-red-700 text-sm font-medium text-white transition"
          >
            {isDeleting ? "Loading" : "Delete"}
            {/* Delete */}
          </button>
        </div>
        </>
      </PopupModal>
      {selectedData&&
      <PopupModal visible={editUserModalVisible} children={<EditUserForm setShowModal={setEditUserModalVisible} data={selectedData}/>}/>
      }
    </div>
  );
}
