import { useState } from "react";
import { useUpdateUser, type IUser } from "../utilities/myQuery";

type UserFormValues = {
  id:string,
  username: string;
  name: string;
  active: boolean;
  role: string;
};

// type UserFormProps = {
//   onSubmit: (values: UserFormValues) => void;
// };
// const active = true

type NewFormProp = {
  setShowModal :React.Dispatch<React.SetStateAction<boolean>>;
  data:IUser
}

export function EditUserForm({ setShowModal,data}: NewFormProp) {

  const {mutate,isPending} = useUpdateUser()
  const [form, setForm] = useState<UserFormValues>({
    id:data.id,
    username: data.username,
    name: data.nama,
    active: data.active,
    role: data.role, // default role
  });

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  function handleToogle(){
    console.log(form)
    setForm((prev) => ({ ...prev, ['active']: !prev.active }));
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    mutate(form,{
      onSuccess:()=>{
        setShowModal(false)
      }
    })
    
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="space-y-4"
    >
          <div>
            <h2 className="text-2xl font-bold text-slate-800">👥 New User</h2>
            <p className="text-sm text-slate-500 mt-1">
              Fill in the details below to add new User.
            </p>
          </div>
      <div>
        <label className="block text-sm font-medium text-gray-700">
          Username
        </label>
        <input
          type="text"
          name="username"
          value={form.username}
          onChange={handleChange}
          className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:ring-blue-500 focus:border-blue-500"
          placeholder="Enter username"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">Name</label>
        <input
          type="text"
          name="name"
          value={form.name}
          onChange={handleChange}
          className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:ring-blue-500 focus:border-blue-500"
          placeholder="Enter full name"
        />
      </div>

      {/* <div>
        <label className="block text-sm font-medium text-gray-700">
          Password
        </label>
        <input
          type="password"
          name="password"
          value={form.password}
          onChange={handleChange}
          className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:ring-blue-500 focus:border-blue-500"
          placeholder="Enter password"
        />
      </div> */}

      <div>
        <label className="block text-sm font-medium text-gray-700">Role</label>
        <select
          name="role"
          value={form.role}
          onChange={handleChange}
          className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:ring-blue-500 focus:border-blue-500"
        >
          <option value="user">User</option>
          {/* <option value="editor">Editor</option> */}
          <option value="admin">Admin</option>
        </select>
      </div>

    <div>
      <span className="block text-sm font-medium text-gray-700">Status</span>
      <div className="flex items-center gap-3">
        <span className={`text-sm ${!form.active ? "text-gray-900" : "text-gray-400"}`}>
          Inactive
        </span>

        <div
          onClick={handleToogle}
          className={`w-12 h-6 flex items-center rounded-full p-1 cursor-pointer transition-colors 
            ${form.active ? "bg-green-500" : "bg-gray-300"}`}
        >
          <div
            className={`bg-white w-4 h-4 rounded-full shadow-md transform transition-transform 
              ${form.active ? "translate-x-6" : "translate-x-0"}`}
          />
        </div>

        <span className={`text-sm ${form.active ? "text-gray-900" : "text-gray-400"}`}>
          Active
        </span>
      </div>


    </div>



    <div className="pt-4 flex justify-end gap-4 border-t border-slate-200">
        <button
          className="px-4 py-2 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium transition"
          onClick={() => setShowModal(false)}
        >
          Cancel
        </button>
        {/* {!result && ( */}
          <button
            className="px-4 py-2 rounded-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold transition"
            onClick={handleSubmit}
          >
            {/* Add */}
            {isPending ? "Loading..." : "Update"}
          </button>
        {/* )} */}
      </div>
    </form>
  );
}