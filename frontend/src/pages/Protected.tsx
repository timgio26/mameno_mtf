import {type ReactNode } from "react";
import { useUserCheck } from "../utilities/myQuery";
import { Loading } from "../components/Loading";
import { Navigate } from "react-router";

type ProtectedProp = {
  children: ReactNode;
};

export function Protected({ children }: ProtectedProp) {
  const { data, isLoading } = useUserCheck();
  
  if (isLoading) return <Loading />;
  
  if (!data?.authenticated) {
    return <Navigate to="/auth" />;
  }

  return children
}
