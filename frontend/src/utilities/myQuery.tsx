import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { toast } from "react-toastify";
import axios from "axios"; 
import { useNavigate } from "react-router";
import { z } from "zod";
import { getCurrentUser } from "./myFunction";
import { useEffect } from "react";

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
        user_id : decoded.sub,
        divisi : data.divisi
      }
      const resp = await axios.post(url,reqBody)
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

export function useGetNota(page:number,search:string|undefined){
  const {data,isLoading,isError} =  useQuery({
    queryKey:["nota",page,search],
    queryFn:async()=>{
      const resp = await axios.get(`api/nota?page=${page}&search=${search}`)
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
  const queryClient = useQueryClient();
  const {mutate,isPending} = useMutation({
    mutationFn:async(id:string)=>{
      const resp = await axios.delete(`api/nota/${id}`)
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
  const queryClient = useQueryClient();
  const {mutate,isPending} = useMutation({
    mutationFn:async(data:IUpdate)=>{
      const resp = await axios.put(`api/nota/${data.id}`,data)
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

export function useGetMemo(page:number,search:string|undefined){
  const {data,isLoading,isError} =  useQuery({
    queryKey:["memo",page,search],
    queryFn:async()=>{
      const resp = await axios.get(`api/memo?page=${page}&search=${search}`)
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
  const {mutate,isPending} = useMutation({
    mutationFn:async(id:string)=>{
      const resp = await axios.delete(`api/memo/${id}`)
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
  const {mutate,isPending} = useMutation({
    mutationFn:async(data:IUpdate)=>{
      const resp = await axios.put(`api/memo/${data.id}`,data)
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

export function useGetPembelian(page:number,search:string|undefined){
  const {data,isLoading,isError} =  useQuery({
    queryKey:["pembelian",page,search],
    queryFn:async()=>{
      const resp = await axios.get(`api/beli?page=${page}&search=${search}`)
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
  const {mutate,isPending} = useMutation({
    mutationFn:async(id:string)=>{
      const resp = await axios.delete(`api/beli/${id}`)
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
  const {mutate,isPending} = useMutation({
    mutationFn:async(data:IUpdate)=>{
      const resp = await axios.put(`api/beli/${data.id}`,data)
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

export function useGetBersama(page:number,search:string|undefined){
  const {data,isLoading,isError} =  useQuery({
    queryKey:["bersama",page,search],
    queryFn:async()=>{
      const resp = await axios.get(`api/bersama?page=${page}&search=${search}`)
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
  const {mutate,isPending} = useMutation({
    mutationFn:async(id:string)=>{
      const resp = await axios.delete(`api/bersama/${id}`)
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
  const {mutate,isPending} = useMutation({
    mutationFn:async(data:IUpdate)=>{
      const resp = await axios.put(`api/bersama/${data.id}`,data)
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