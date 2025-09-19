import { Navigate } from "react-router-dom";
import { useAuth } from "@/context/AuthContext";
import { JSX } from "react/jsx-dev-runtime";

export const ProtectedRoute = ({ children }: { children: JSX.Element }) => {
  const { token } = useAuth();
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  return children;
};
