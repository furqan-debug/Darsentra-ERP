import React from "react";
import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useAuth } from "@/context/AuthContext";
import { School } from "lucide-react";

export const ProtectedRoute: React.FC = () => {
  const { isAuthenticated, isLoading, hasSchool } = useAuth();
  const location = useLocation();

  if (isLoading) {
    return (
      <div className="min-h-[60vh] flex flex-col items-center justify-center space-y-4">
        <div className="h-12 w-12 rounded-2xl bg-teal-700 text-white flex items-center justify-center animate-pulse shadow-md">
          <School className="h-6 w-6" />
        </div>
        <div className="text-sm font-medium text-slate-600 dark:text-slate-400">
          Loading workspace...
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  if (!hasSchool && location.pathname !== "/setup-school") {
    return <Navigate to="/setup-school" replace />;
  }

  return <Outlet />;
};

export default ProtectedRoute;
