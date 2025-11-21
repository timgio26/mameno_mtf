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

const AddDataRespSchema = z.object({
  // id:z.string(),
  no_nota:z.string()

})

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
        user_id : decoded.sub
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

const NotaRespSchema = z.object({data:z.array(NotaSchema)})

export function useGetNota(){
  const {data,isLoading,isError} =  useQuery({
    queryKey:["nota"],
    queryFn:async()=>{
      const resp = await axios.get('api/nota')
      return resp.data
    },
    retry:false
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
  
  return {
    data: parseResult.data?.data,
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

const BeliRespSchema = z.object({data:z.array(BeliSchema)})

export function useGetPembelian(){
  const {data,isLoading,isError} =  useQuery({
    queryKey:["pembelian"],
    queryFn:async()=>{
      const resp = await axios.get('api/beli')
      return resp.data
    }
  })
  
  const parseResult = BeliRespSchema.safeParse(data);
  if(isError || !parseResult.success){
    toast.error("Can't load data, please try again later")
  }

  
  return {
    data: parseResult.data?.data,
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

const BersamaRespSchema = z.object({data:z.array(BersamaSchema)})

export function useGetBersama(){
  const {data,isLoading,isError} =  useQuery({
    queryKey:["bersama"],
    queryFn:async()=>{
      const resp = await axios.get('api/bersama')
      return resp.data
    }
  })
  
  const parseResult = BersamaRespSchema.safeParse(data);
  console.log(parseResult)
  if(isError || !parseResult.success){
    toast.error("Can't load data, please try again later")
  }

  
  return {
    data: parseResult.data?.data,
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