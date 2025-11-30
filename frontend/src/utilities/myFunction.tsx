import axios from "axios";
import { jwtDecode } from "jwt-decode";
import Cookies from "js-cookie";

export function getCurrentUser(){
    const token = sessionStorage.getItem("token");
    if(!token) throw new Error('no token')
    const decoded= jwtDecode(token)
    return {token,decoded}
}

export const api = axios.create();
//   baseURL: "/api", // Vite proxy forwards to Flask
//   withCredentials: true // ensures cookies are sent
// });
// reference: https://axios-http.com/docs/instance
api.interceptors.response.use(
  undefined,
  async (err) => {
    const csrfToken = Cookies.get("csrf_access_token");
    if (err.response?.status === 401) {
      try {
        await api.post("/refresh",undefined,{withCredentials:true,headers: { "X-CSRF-TOKEN": csrfToken }});
        return api(err.config); // retry original request
      } catch {
        window.location.href = "/auth"; // refresh failed
      }
    }
    throw err; // just rethrow other errors
  }
);




export function get_today_date(){
    const today = new Date();
    return today.toISOString().split("T")[0]
}
