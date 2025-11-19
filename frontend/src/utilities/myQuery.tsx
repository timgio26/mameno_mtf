import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { toast } from "react-toastify";
import axios from "axios"; 
import { useNavigate } from "react-router";
import { z } from "zod";
import { getCurrentUser } from "./myFunction";

type SignupDto = {
  username: string;
  name:string;
  password: string;
};

type SigninDto = {
  username: string;
  password: string;
};

const SigninRespSchema = z.object({
  token : z.string()
})


export function useSignUp(){
  const {mutate,isError,isPending} = useMutation({
    mutationFn:async(data:SignupDto)=>{
      const resp = await axios.post('api/signup',data)
      if(resp.status!=201){
        throw new Error("signup error")
      }
    },
    onError:()=>{
      toast.error("Can't signup try again later")
    },
    onSuccess:()=>{
      toast.success("Signup success! Please Login")
    }

  })
  return {mutate,isError,isPending}
}

export function useSignIn(){
  const navigate = useNavigate()
  const {mutate,isError,isPending} = useMutation({
    mutationFn:async(data:SigninDto)=>{
      const resp = await axios.post('api/login',data)
      if(resp.status!=200){
        throw new Error("Signin error")
      }
      const parsed = SigninRespSchema.safeParse(resp.data)
      if(!parsed.success){
        throw new Error("signup error")
      }
      return parsed.data
    },
    onError:()=>{
      toast.error("Can't Login. Try again later")
    },
    onSuccess:(fromMutation)=>{
      toast.success("Login Success")
      sessionStorage.setItem('token',fromMutation.token)
      navigate("/")
    }
  })
  return {mutate,isError,isPending}
}

type IAddData = {
  judul:string;
  // type:string;
  divisi?:string[];
}

export function useAddData(type:string|undefined){
  const queryClient = useQueryClient();
  const {mutate,isPending} = useMutation({
    mutationFn:async(data:IAddData)=>{
      const {token,decoded} = getCurrentUser()
      let url
      if(type == "nota"){
        url = "api/nota"
      }else if(type=="memo"){
        url = "api/memo"
      }else if(type=="pembelian"){
        url = "api/beli"
      }else if(type=="bersama"){
        url = "api/bersama"
      }else{
        throw new Error("type unrecognized")
      }
      const reqBody = {
        judul : data.judul,
        user_id : decoded.sub
      }
      const resp = await axios.post(url,reqBody)
      return resp.data
    },
    onError:()=>{
      toast.error("Can't add data, try again later")
    },
    onSuccess:()=>{
      queryClient.invalidateQueries({ queryKey: [type] });
      toast.success("Data added")
    }
  })
  return {mutate,isPending}
}

const NotaSchema = z.object({
  id:z.string(),
  judul_nota:z.string(),
  link_nota:z.string().nullable(),
  no:z.number(),
  no_nota:z.string(),
  penulis_nota:z.string(),
  tanggal_buat:z.string(),
})

const NotaRespSchema = z.object({data:z.array(NotaSchema)})

export function useGetNota(){
  const {data,isLoading,isError} =  useQuery({
    queryKey:["nota"],
    queryFn:async()=>{
      const resp = await axios.get('api/nota')
      return resp.data
    }
  })

  if(isError){
    toast.error("Can't load data, please try again later")
  }

  const parseResult = NotaRespSchema.safeParse(data);
  
  return {
    data: parseResult.data?.data,
    isLoading,
    isError
  };

}



const MemoSchema = z.object({
  id:z.string(),
  judul_memo:z.string(),
  link_memo:z.string().nullable(),
  no:z.number(),
  no_memo:z.string(),
  penulis_memo:z.string(),
  tanggal_buat:z.string(),
})

const MemoRespSchema = z.object({data:z.array(MemoSchema)})


export function useGetMemo(){
  const {data,isLoading,isError} =  useQuery({
    queryKey:["memo"],
    queryFn:async()=>{
      const resp = await axios.get('api/memo')
      return resp.data
    }
  })

  if(isError){
    toast.error("Can't load data, please try again later")
  }
  

  const parseResult = MemoRespSchema.safeParse(data);

  console.log(data,parseResult)
  
  return {
    data: parseResult.data?.data,
    isLoading,
    isError
  };

}