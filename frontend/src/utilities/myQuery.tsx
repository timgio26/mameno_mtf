import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { toast } from "react-toastify";
import { useNavigate } from "react-router";
import { z } from "zod";
import { useEffect } from "react";
import Cookies from 'js-cookie'
import {api, get_today_date } from "./myFunction"

type SignupDto = {
  username: string;
  name:string;
  password: string;
  role:string;
};

type SigninDto = {
  username: string;
  password: string;
};

const SigninRespSchema = z.object({
  message : z.string(),
  user:z.object({
    nama:z.string(),
    username:z.string(),
    user_id:z.string()
  })
})


export function useSignUp(){
  const queryClient = useQueryClient();
  const {mutate,isError,isPending} = useMutation({
    mutationFn:async(data:SignupDto)=>{
      const csrfToken = Cookies.get("csrf_access_token");
      const resp = await api.post('api/signup',data,{withCredentials:true,headers: { "X-CSRF-TOKEN": csrfToken }})
      if(resp.status!=201){
        throw new Error("signup error")
      }
    },
    onError:()=>{
      toast.error("Can't signup try again later")
    },
    onSuccess:()=>{
      toast.success("User added!")
      queryClient.invalidateQueries({ queryKey: ["user"] });
    }

  })
  return {mutate,isError,isPending}
}


export function useSignIn(){
  const queryClient = useQueryClient();
  const navigate = useNavigate()
  const {mutate,isError,isPending} = useMutation({
    mutationFn:async(data:SigninDto)=>{
      const resp = await api.post('api/login',data)
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
      sessionStorage.setItem('user_id',fromMutation.user.user_id)
      queryClient.invalidateQueries({ queryKey: ["userCheck"] });
      navigate("/")
    }
  })
  return {mutate,isError,isPending}
}

export function useLogOut(){
  const nav = useNavigate()
  const {mutate,isPending} = useMutation({
    mutationFn:async()=>{
      const resp = await api.post('api/logout')
      if(resp.status!=200){
        throw new Error("can't logout")
      }
    },
    onError:()=>{
      toast.error("Can't logout try again later")
    },
    onSuccess:()=>{
      sessionStorage.clear()
      toast.success("Success Log out")
      nav('/auth')
    }
  })
  return {mutate,isPending}
}

const UserCheckResp = z.object({
  authenticated:z.boolean(),
  user_id:z.string(),
  role:z.string(),
})

export function useUserCheck(){
  const {data,isLoading} = useQuery({
    queryKey:["userCheck"],
    queryFn:async()=>{
      const resp = await api.get('/api/me',{withCredentials:true})
      
      if(resp.status!=200){
        throw new Error("user not authenticated")
      }
      const parseResult = UserCheckResp.safeParse(resp.data)
      if(!parseResult.success){
        throw new Error("user not authenticated")
      }
      return parseResult.data
    },
    retry:false,
    staleTime:5 * 60 * 1000
  })
  return {data,isLoading}
}

type IAddData = {
  judul:string;
  // type:string;
  divisi?:string[];
}

const AddDataRespSchema = z.object({
  // id:z.string(),
  no_doc:z.string(),
  pic:z.string(),
  judul:z.string()

})

export type IAddDataResp = z.infer<typeof AddDataRespSchema>;

export function useAddData(type:string|undefined){
  const queryClient = useQueryClient();
  const {data,mutate,isPending} = useMutation({
    mutationFn:async(data:IAddData)=>{
      const csrfToken = Cookies.get("csrf_access_token");
      const user_id = sessionStorage.getItem("user_id");

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
        user_id : user_id,
        divisi : data.divisi
      }
      const resp = await api.post(url,reqBody,{withCredentials:true,headers: { "X-CSRF-TOKEN": csrfToken }})
      const parseResult = AddDataRespSchema.safeParse(resp.data)
      return parseResult.data
    },
    onError:()=>{
      toast.error("Can't add data, try again later")
    },
    onSuccess:()=>{
      queryClient.invalidateQueries({ queryKey: [type] });
      toast.success("Data added")
    }
  })
  return {mutate,isPending,data}
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

export type INota = z.infer<typeof NotaSchema>;

const NotaRespSchema = z.object({
  data:z.array(NotaSchema),
  page:z.number(),
  total_pages:z.number()
})

export function useGetNota(page:number,search:string){
  const {data,isLoading,isError} =  useQuery({
    queryKey:["nota",page,search],
    queryFn:async()=>{
      const resp = await api.get(`api/nota?page=${page}&search=${search}`,{withCredentials:true})
      return resp.data
    },
    retry:false
  })

  const parseResult = NotaRespSchema.safeParse(data);

    useEffect(()=>{
    if(!isError){
      return;
    }
    if(isError||!parseResult.success){
      toast.error("Can't load data, please try again later 2")
    }
  },[isError,parseResult.success])
  
  return {
    data: parseResult.data,
    isLoading,
    isError
  };

}


export function useDelNota(){
  const csrfToken = Cookies.get("csrf_access_token");
  const queryClient = useQueryClient();
  const {mutate,isPending} = useMutation({
    mutationFn:async(id:string)=>{
      const resp = await api.delete(`api/nota/${id}`,{withCredentials:true,headers: { "X-CSRF-TOKEN": csrfToken }})
      if(resp.status!=200){
        throw new Error("Can't delete data, try again later")
      }
    },
    onError:(e)=>{
      toast.error(e.message)
    },
    onSuccess:()=>{
      queryClient.invalidateQueries({ queryKey: ['nota'] });
      toast.success("Data deleted")
    }
  })
  return {mutate,isPending}
}

type IUpdate = {
  id:string;
  judul:string;
  url:string|null|undefined; 
}

export function useUpdateNota(){
  const csrfToken = Cookies.get("csrf_access_token");
  const queryClient = useQueryClient();
  const {mutate,isPending} = useMutation({
    mutationFn:async(data:IUpdate)=>{
      const resp = await api.put(`api/nota/${data.id}`,data,{withCredentials:true,headers: { "X-CSRF-TOKEN": csrfToken }})
      if(resp.status!=200){
        throw new Error("Can't update data, try again later.")
      }
    },
    onError:(e)=>{
      toast.error(e.message)
    },
    onSuccess:()=>{
      queryClient.invalidateQueries({ queryKey: ['nota'] });
      toast.success("Data updated")
    }
  })
  return {mutate,isPending}
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

export type IMemo = z.infer<typeof MemoSchema>;

const MemoRespSchema = z.object({data:z.array(MemoSchema),
  page:z.number(),
  total_pages:z.number(),
})

export function useGetMemo(page:number,search:string){
  const {data,isLoading,isError} =  useQuery({
    queryKey:["memo",page,search],
    queryFn:async()=>{
      const resp = await api.get(`api/memo?page=${page}&search=${search}`,{withCredentials:true})
      return resp.data
    }
  })

  
  const parseResult = MemoRespSchema.safeParse(data);

    useEffect(()=>{
    if(!isError){
      return;
    }
    if(isError||!parseResult.success){
      toast.error("Can't load data, please try again later 2")
    }
  },[isError,parseResult.success])
  
  return {
    data: parseResult.data,
    isLoading,
    isError
  };

}

export function useDelMemo(){
  const queryClient = useQueryClient();
  const csrfToken = Cookies.get("csrf_access_token");
  const {mutate,isPending} = useMutation({
    mutationFn:async(id:string)=>{
      const resp = await api.delete(`api/memo/${id}`,{withCredentials:true,headers: { "X-CSRF-TOKEN": csrfToken }})
      if(resp.status!=200){
        throw new Error("Can't delete data, try again later")
      }
    },
    onError:(e)=>{
      toast.error(e.message)
    },
    onSuccess:()=>{
      queryClient.invalidateQueries({ queryKey: ['memo'] });
      toast.success("Data deleted")
    }
  })
  return {mutate,isPending}
}

export function useUpdateMemo(){
  const queryClient = useQueryClient();
  const csrfToken = Cookies.get("csrf_access_token");
  const {mutate,isPending} = useMutation({
    mutationFn:async(data:IUpdate)=>{
      const resp = await api.put(`api/memo/${data.id}`,data,{withCredentials:true,headers: { "X-CSRF-TOKEN": csrfToken }})
      if(resp.status!=200){
        throw new Error("Can't update data, try again later.")
      }
    },
    onError:(e)=>{
      toast.error(e.message)
    },
    onSuccess:()=>{
      queryClient.invalidateQueries({ queryKey: ['memo'] });
      toast.success("Data updated")
    }
  })
  return {mutate,isPending}
}

const BeliSchema = z.object({
  id:z.string(),
  judul_beli:z.string(),
  link_beli:z.string().nullable(),
  no:z.number(),
  no_beli:z.string(),
  penulis_beli:z.string(),
  tanggal_buat:z.string(),
})

export type IBeli = z.infer<typeof BeliSchema>;

const BeliRespSchema = z.object({data:z.array(BeliSchema),
  page:z.number(),
  total_pages:z.number()
})

export function useGetPembelian(page:number,search:string){
  const {data,isLoading,isError} =  useQuery({
    queryKey:["pembelian",page,search],
    queryFn:async()=>{
      const resp = await api.get(`api/beli?page=${page}&search=${search}`,{withCredentials:true})
      return resp.data
    },

  })

  const parseResult = BeliRespSchema.safeParse(data);
  useEffect(()=>{
    if(!isError){
      return;
    }
    if(isError||!parseResult.success){
      toast.error("Can't load data, please try again later 2")
    }
  },[isError,parseResult.success])

  return {
    data: parseResult.data,
    isLoading,
    isError
  };

}

export function useDelPembelian(){
  const queryClient = useQueryClient();
  const csrfToken = Cookies.get("csrf_access_token");
  const {mutate,isPending} = useMutation({
    mutationFn:async(id:string)=>{
      const resp = await api.delete(`api/beli/${id}`,{withCredentials:true,headers: { "X-CSRF-TOKEN": csrfToken }})
      if(resp.status!=200){
        throw new Error("Can't delete data, try again later")
      }
    },
    onError:(e)=>{
      toast.error(e.message)
    },
    onSuccess:()=>{
      queryClient.invalidateQueries({ queryKey: ['pembelian'] });
      toast.success("Data deleted")
    }
  })
  return {mutate,isPending}
}


export function useUpdatePembelian(){
  const queryClient = useQueryClient();
  const csrfToken = Cookies.get("csrf_access_token");
  const {mutate,isPending} = useMutation({
    mutationFn:async(data:IUpdate)=>{
      const resp = await api.put(`api/beli/${data.id}`,data,{withCredentials:true,headers: { "X-CSRF-TOKEN": csrfToken }})
      if(resp.status!=200){
        throw new Error("Can't update data, try again later.")
      }
    },
    onError:(e)=>{
      toast.error(e.message)
    },
    onSuccess:()=>{
      queryClient.invalidateQueries({ queryKey: ['pembelian'] });
      toast.success("Data updated")
    }
  })
  return {mutate,isPending}
}



const BersamaSchema = z.object({
  id:z.string(),
  judul:z.string(),
  link:z.string().nullable(),
  no:z.number(),
  no_bersama:z.string(),
  penulis:z.string(),
  tanggal_buat:z.string(),
})

export type IBersama = z.infer<typeof BersamaSchema>;

const BersamaRespSchema = z.object({data:z.array(BersamaSchema),
  page:z.number(),
  total_pages:z.number()
})

export function useGetBersama(page:number,search:string){
  const {data,isLoading,isError} =  useQuery({
    queryKey:["bersama",page,search],
    queryFn:async()=>{
      const resp = await api.get(`api/bersama?page=${page}&search=${search}`,{withCredentials:true})
      return resp.data
    }
  })
  
  const parseResult = BersamaRespSchema.safeParse(data);
  useEffect(()=>{
    if(!isError){
      return;
    }
    if(isError||!parseResult.success){
      toast.error("Can't load data, please try again later 2")
    }
  },[isError,parseResult.success])
  // console.log(parseResult.data?.data)
  return {
    data: parseResult.data,
    isLoading,
    isError
  };

}

export function useDelBersama(){
  const queryClient = useQueryClient();
  const csrfToken = Cookies.get("csrf_access_token");
  const {mutate,isPending} = useMutation({
    mutationFn:async(id:string)=>{
      const resp = await api.delete(`api/bersama/${id}`,{withCredentials:true,headers: { "X-CSRF-TOKEN": csrfToken }})
      if(resp.status!=200){
        throw new Error("Can't delete data, try again later")
      }
    },
    onError:(e)=>{
      toast.error(e.message)
    },
    onSuccess:()=>{
      queryClient.invalidateQueries({ queryKey: ['bersama'] });
      toast.success("Data deleted")
    }
  })
  return {mutate,isPending}
}

export function useUpdateBersama(){
  const queryClient = useQueryClient();
  const csrfToken = Cookies.get("csrf_access_token");
  const {mutate,isPending} = useMutation({
    mutationFn:async(data:IUpdate)=>{
      const resp = await api.put(`api/bersama/${data.id}`,data,{withCredentials:true,headers: { "X-CSRF-TOKEN": csrfToken }})
      if(resp.status!=200){
        throw new Error("Can't update data, try again later.")
      }
    },
    onError:(e)=>{
      toast.error(e.message)
    },
    onSuccess:()=>{
      queryClient.invalidateQueries({ queryKey: ['bersama'] });
      toast.success("Data updated")
    }
  })
  return {mutate,isPending}
}

export async function downloadData(){
  try {
    // const token = sessionStorage.getItem("token");
    const response = await api.get('api/download',{withCredentials:true,responseType:"blob"});
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `Mameno ${get_today_date()}.xlsx`);
    document.body.appendChild(link);
    link.click();
    link.remove();
    toast.success("File downloaded");
  } catch (error) {
    toast.error("Can't download")
  }
};
const UserSchema = z.object({
  id:z.string(),
  nama:z.string(),
  role:z.string(),
  username:z.string(),
  active:z.boolean()
})
const AllUserRespSchema = z.object({
  data:z.array(UserSchema),
  page:z.number(),
  total_pages:z.number()
})
export type IUser = z.infer<typeof UserSchema>;
export function useGetUser(page:number){
  const {data,isError,isLoading} = useQuery({
    queryKey:['user',page],
    queryFn:async()=>{
      const resp = await api.get(`/api/user?page=${page}`,{withCredentials:true})
      // console.log(resp.data)
      return resp.data
    }
  })

  const parseResult = AllUserRespSchema.safeParse(data)
  // console.log(parseResult)

  useEffect(()=>{
    if(!isError){
      return;
    }
    if(isError||!parseResult.success){
      toast.error("Can't load data, please try again later 2")
    }
  },[isError,parseResult.success])

  return {data:parseResult.data,isError,isLoading}
}


export function useDelUser(){
  const queryClient = useQueryClient();
  const csrfToken = Cookies.get("csrf_access_token");
  const {mutate,isPending} = useMutation({
    mutationFn:async(id:string)=>{
      const resp = await api.delete(`api/user/${id}`,{withCredentials:true,headers: { "X-CSRF-TOKEN": csrfToken }})
      if(resp.status!=200){
        throw new Error("Can't delete data, try again later")
      }
    },
    onError:(e)=>{
      toast.error(e.message)
    },
    onSuccess:()=>{
      queryClient.invalidateQueries({ queryKey: ['user'] });
      toast.success("Data deleted")
    }
  })
  return {mutate,isPending}
}

type IUpdateUser = {
  id:string,
  username: string;
  name: string;
  active: boolean;
  role: string;
}

export function useUpdateUser(){
  const csrfToken = Cookies.get("csrf_access_token");
  const queryClient = useQueryClient();
  const {mutate,isPending} = useMutation({
    mutationFn:async(data:IUpdateUser)=>{
      const resp = await api.put(`api/user/${data.id}`,data,{withCredentials:true,headers: { "X-CSRF-TOKEN": csrfToken }})
      if(resp.status!=200){
        throw new Error("Can't update data, try again later.")
      }
    },
    onError:(e)=>{
      toast.error(e.message)
    },
    onSuccess:()=>{
      queryClient.invalidateQueries({ queryKey: ['user'] });
      toast.success("Data updated")
    }
  })
  return {mutate,isPending}
}