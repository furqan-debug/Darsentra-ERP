import React from "react";
import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "@/context/AuthContext";

export const PublicOnlyRoute: React.FC = () => {
  const { isAuthenticated, isLoading, hasSchool } = useAuth();

  if (isLoading) {
    return null;
  }

  if (isAuthenticated) {
    if (!hasSchool) {
      return <Navigate to="/setup-school" replace />;
    }
    return <Navigate to="/dashboard" replace />;
  }

  return <Outlet />;
};

export default PublicOnlyRoute;
