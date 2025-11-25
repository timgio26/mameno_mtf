import { useState } from "react";

type UserFormValues = {
  username: string;
  name: string;
  password: string;
  role: string;
};

type UserFormProps = {
  onSubmit: (values: UserFormValues) => void;
};

type NewFormProp = {
  setShowModal :React.Dispatch<React.SetStateAction<boolean>>
}

export function NewUserForm({ setShowModal }: NewFormProp) {
  const [form, setForm] = useState<UserFormValues>({
    username: "",
    name: "",
    password: "",
    role: "user", // default role
  });

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // onSubmit(form);
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

      <div>
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
      </div>

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
            // onClick={submitForm}
          >
            Add
            {/* {isPending ? "Loading..." : "Submit"} */}
          </button>
        {/* )} */}
      </div>
    </form>
  );
}