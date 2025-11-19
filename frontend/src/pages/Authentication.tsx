import React, { useState } from "react";
import { useSignUp,useSignIn} from "../utilities/myQuery";

type AuthMode = "login" | "signup";

interface LoginFormState {
  username: string;
  password: string;
}

interface SignupFormState extends LoginFormState {
  name: string;
}

export function Authentication() {
  const [mode, setMode] = useState<AuthMode>("login");
  const [loginForm, setLoginForm] = useState<LoginFormState>({
    username: "",
    password: "",
  });
  const [signupForm, setSignupForm] = useState<SignupFormState>({
    name: "",
    username: "",
    password: "",
  });
  const { mutate: signUp, isPending: loadingSignUp } = useSignUp();
  const { mutate: signIn, isPending: loadingSignIn } = useSignIn();
  const [showPwd, setShowPdw] = useState<boolean>(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    if (mode === "login") {
      setLoginForm({ ...loginForm, [name]: value });
    } else {
      setSignupForm({ ...signupForm, [name]: value });
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (mode === "login") {
      console.log('Logging in with', loginForm);
      signIn(loginForm);
    } else {
      console.log('Signing up with', signupForm);
      signUp(signupForm, {
        onSuccess: () => {
          setMode("login");
        },
      });
    }
  };

  return (
    <div className="flex items-center justify-center p-6">
      <div className="bg-white rounded-3xl shadow-2xl p-10 w-full max-w-md">
        <h2 className="text-3xl font-bold text-gray-800 mb-6 text-center">
          {mode === "login" ? "Welcome Back 👋" : "Create an Account 🚀"}
        </h2>

        <form onSubmit={handleSubmit} className="space-y-5">
          {mode === "signup" && (
            <div>
              <label
                htmlFor="name"
                className="block text-sm font-medium text-gray-700"
              >
                Name
              </label>
              <input
                type="text"
                name="name"
                id="name"
                value={signupForm.name}
                onChange={handleChange}
                required
                className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:ring-pink-500 focus:border-pink-500"
              />
            </div>
          )}

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
                mode === "login" ? loginForm.username : signupForm.username
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
                  mode === "login" ? loginForm.password : signupForm.password
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
            {loadingSignUp || loadingSignIn
              ? "Loading..."
              : mode === "login"
              ? "Login"
              : "Sign Up"}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-gray-600">
          {mode === "login"
            ? "Don't have an account?"
            : "Already have an account?"}{" "}
          <button
            type="button"
            onClick={() => setMode(mode === "login" ? "signup" : "login")}
            className="text-indigo-600 hover:underline font-medium"
          >
            {mode === "login" ? "Sign up" : "Login"}
          </button>
        </p>
      </div>
    </div>
  );
}