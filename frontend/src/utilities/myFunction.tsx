import { jwtDecode } from "jwt-decode";
export function getCurrentUser(){
    const token = sessionStorage.getItem("token");
    if(!token) throw new Error('no token')
    const decoded= jwtDecode(token)
    return {token,decoded}
}