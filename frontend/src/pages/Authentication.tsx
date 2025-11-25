import React, { useState } from "react";
import { useSignIn} from "../utilities/myQuery";



interface LoginFormState {
  username: string;
  password: string;
}



export function Authentication() {
  // const [mode, setMode] = useState<AuthMode>("login");
  const [loginForm, setLoginForm] = useState<LoginFormState>({
    username: "",
    password: "",
  });

  const { mutate: signIn, isPending: loadingSignIn } = useSignIn();
  const [showPwd, setShowPdw] = useState<boolean>(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;

      setLoginForm({ ...loginForm, [name]: value });

  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    signIn(loginForm);

  };

  return (
    <div className="flex items-center justify-center p-6">
      <div >
        <h2 className="text-3xl font-bold text-gray-800 mb-6 text-center">
          Welcome Back 👋

        </h2>

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label
              htmlFor="username"
              className="block text-sm font-medium text-gray-700"
            >
              Username
            </label>
            <input
              type="text"
              name="username"
              id="username"
              value={
                loginForm.username
              }
              onChange={handleChange}
              required
              className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
            />
          </div>

          <div>
            <label
              htmlFor="password"
              className="block text-sm font-medium text-gray-700"
            >
              Password
            </label>
            <div className="relative">
              <input
                type={showPwd ? "text" : "password"}
                name="password"
                id="password"
                value={
                  loginForm.password 
                }
                onChange={handleChange}
                required
                className="w-full px-4 py-2 pr-12 border border-gray-300 rounded-lg shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
              />
              <button
                type="button"
                onClick={() => setShowPdw((curstate) => !curstate)}
                className="absolute inset-y-0 right-0 px-3 flex items-center text-sm text-gray-600 hover:text-indigo-600 focus:outline-none"
              >
                {showPwd ? "Hide" : "Show"}
              </button>
            </div>
          </div>

          <button
            type="submit"
            className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-4 rounded-lg transition duration-300"
          >
            {loadingSignIn?"Loading...":"Login"}

          </button>
        </form>
      </div>
    </div>
  );
}