import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter,Routes,Route } from "react-router";
import { Base } from './pages/Base';
import './index.css'
// import { Homepage } from './pages/Homepage';
import { Authentication } from './pages/Authentication';
import { ToastContainer } from "react-toastify";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Nota } from './pages/Nota';
import { Memo } from './pages/Memo';
import { Pembelian } from './pages/Pembelian';
import { NotaBersama } from './pages/NotaBersama';
import { Protected } from './pages/Protected';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import { User } from './pages/User';

const queryClient = new QueryClient();


createRoot(document.getElementById('root')!).render(
  <StrictMode>
    
    <QueryClientProvider client={queryClient}>

    <BrowserRouter>
    <Routes>
      <Route element={<Protected><Base/></Protected>}>
        <Route path="/" element={<Nota/>}/>
        <Route path="/memo" element={<Memo/>}/>
        <Route path="/pembelian" element={<Pembelian/>}/>
        <Route path="/bersama" element={<NotaBersama/>}/>
        <Route path="/user" element={<User/>}/>
      </Route>
      <Route path="/auth" element={<Authentication/>}/>
    </Routes>

    </BrowserRouter>

    <ReactQueryDevtools initialIsOpen={false} />

    </QueryClientProvider>
    <ToastContainer
        position="top-center"
        autoClose={3000}
        hideProgressBar
        closeOnClick
        pauseOnHover
        theme="light"
      />
  </StrictMode>,
)
