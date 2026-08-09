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

<div className="min-h-screen bg-linear-to-br from-slate-50 via-white to-blue-50 px-4 py-8 sm:px-6">
  <div className="flex min-h-[calc(100vh-4rem)] items-center justify-center">
    <div className="w-full max-w-md">
      {/* Login Card */}
      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-xl shadow-slate-200/50 sm:p-8">
        
        {/* Header */}
        <div className="mb-8 text-center">
          {/* Optional logo */}
          {/* {logo && (
            <div className="mb-5 flex justify-center">
              <img
                src={logo}
                alt="AR APP Logo"
                className="h-16 w-16 rounded-2xl object-cover shadow-md"
              />
            </div>
          )} */}

          <h2 className="text-2xl font-bold tracking-tight text-slate-900 sm:text-3xl">
            Welcome Back
          </h2>

          <p className="mt-2 text-sm text-slate-500">
            Sign in to continue to AR APP
          </p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-5">
          {/* Username */}
          <div>
            <label
              htmlFor="username"
              className="mb-2 block text-sm font-semibold text-slate-700"
            >
              Username
            </label>

            <input
              type="text"
              name="username"
              id="username"
              value={loginForm.username}
              onChange={handleChange}
              required
              autoComplete="username"
              placeholder="Enter your username"
              className="w-full rounded-xl border border-slate-300 bg-slate-50 px-4 py-3 text-sm text-slate-900 outline-none transition placeholder:text-slate-400 hover:border-slate-400 focus:border-blue-500 focus:bg-white focus:ring-4 focus:ring-blue-500/10"
            />
          </div>

          {/* Password */}
          <div>
            <label
              htmlFor="password"
              className="mb-2 block text-sm font-semibold text-slate-700"
            >
              Password
            </label>

            <div className="relative">
              <input
                type={showPwd ? "text" : "password"}
                name="password"
                id="password"
                value={loginForm.password}
                onChange={handleChange}
                required
                autoComplete="current-password"
                placeholder="Enter your password"
                className="w-full rounded-xl border border-slate-300 bg-slate-50 px-4 py-3 pr-16 text-sm text-slate-900 outline-none transition placeholder:text-slate-400 hover:border-slate-400 focus:border-blue-500 focus:bg-white focus:ring-4 focus:ring-blue-500/10"
              />

              <button
                type="button"
                onClick={() => setShowPdw((curstate) => !curstate)}
                className="absolute inset-y-0 right-0 px-4 text-sm font-medium text-slate-500 transition hover:text-blue-600 focus:outline-none focus:text-blue-600"
                aria-label={showPwd ? "Hide password" : "Show password"}
              >
                {showPwd ? "Hide" : "Show"}
              </button>
            </div>
          </div>

          {/* Login Button */}
          <button
            type="submit"
            disabled={loadingSignIn}
            className="flex w-full items-center justify-center rounded-xl bg-blue-600 px-4 py-3 text-sm font-semibold text-white shadow-lg shadow-blue-600/20 transition-all duration-200 hover:bg-blue-700 hover:shadow-blue-600/30 focus:outline-none focus:ring-4 focus:ring-blue-500/20 active:scale-[0.99] disabled:cursor-not-allowed disabled:bg-blue-400 disabled:shadow-none"
          >
            {loadingSignIn ? (
              <>
                <svg
                  className="mr-2 h-4 w-4 animate-spin"
                  viewBox="0 0 24 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  />

                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
                  />
                </svg>

                Signing in...
              </>
            ) : (
              "Login"
            )}
          </button>
        </form>

        {/* Footer */}
        <div className="mt-8 border-t border-slate-100 pt-5 text-center">
          <p className="text-xs text-slate-400">
            AR MTF &copy; {new Date().getFullYear()}
          </p>
        </div>
      </div>
    </div>
  </div>
</div>


  );
}