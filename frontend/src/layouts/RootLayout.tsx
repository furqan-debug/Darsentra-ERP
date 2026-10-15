import React from "react";
import { Link, Outlet, useNavigate } from "react-router-dom";
import {
  Building2,
  CheckCircle2,
  LogOut,
  School,
  ShieldCheck,
  User,
  XCircle,
} from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/context/AuthContext";
import { useHealthCheck } from "@/hooks/useHealthCheck";

export const RootLayout: React.FC = () => {
  const { user, isAuthenticated, activeSchool, activeRoleDisplay, logout } = useAuth();
  const { data: health, isLoading: healthLoading } = useHealthCheck();
  const navigate = useNavigate();

  const isHealthy = health?.status === "healthy" && health.database.status === "connected";

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100">
      {/* Top Navigation Bar */}
      <header className="sticky top-0 z-40 w-full border-b border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          {/* Logo & School Context */}
          <div className="flex items-center space-x-3">
            <Link
              to={isAuthenticated ? "/dashboard" : "/"}
              className="flex items-center space-x-2.5"
            >
              <div className="h-9 w-9 rounded-xl bg-teal-700 text-white flex items-center justify-center shadow-sm">
                <School className="h-5 w-5" />
              </div>
              <div>
                <span className="text-lg font-extrabold tracking-tight text-slate-900 dark:text-white">
                  Darsentra
                </span>
                <span className="text-[10px] text-teal-700 dark:text-teal-400 font-bold ml-1 uppercase">
                  ERP
                </span>
              </div>
            </Link>

            {isAuthenticated && activeSchool && (
              <div className="hidden md:flex items-center pl-3 ml-3 border-l border-slate-200 dark:border-slate-700 space-x-2">
                <Building2 className="h-4 w-4 text-teal-600" />
                <span className="text-xs font-semibold text-slate-700 dark:text-slate-200 max-w-[200px] truncate">
                  {activeSchool.name}
                </span>
                <Badge variant="outline" className="text-[10px] font-mono border-teal-600 text-teal-700 dark:text-teal-300">
                  {activeSchool.code}
                </Badge>
              </div>
            )}
          </div>

          {/* Right Header Navigation & Actions */}
          <div className="flex items-center space-x-3">
            {/* System Health Pill */}
            <div className="hidden lg:flex items-center space-x-1 px-2.5 py-1 rounded-full text-[11px] bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700">
              {healthLoading ? (
                <div className="h-2 w-2 rounded-full bg-amber-400 animate-pulse mr-1" />
              ) : isHealthy ? (
                <CheckCircle2 className="h-3 w-3 text-emerald-500 mr-1" />
              ) : (
                <XCircle className="h-3 w-3 text-red-500 mr-1" />
              )}
              <span className="text-slate-600 dark:text-slate-300">
                {healthLoading ? "Checking..." : isHealthy ? "API Online" : "API Offline"}
              </span>
            </div>

            {isAuthenticated ? (
              <div className="flex items-center space-x-3">
                <div className="text-right hidden sm:block">
                  <div className="text-xs font-semibold text-slate-900 dark:text-white">
                    {user?.full_name || user?.email}
                  </div>
                  <div className="text-[10px] text-teal-700 dark:text-teal-400 font-medium">
                    {activeRoleDisplay || "School Staff"}
                  </div>
                </div>

                <div className="h-8 w-8 rounded-full bg-teal-100 dark:bg-teal-900/60 text-teal-800 dark:text-teal-300 flex items-center justify-center font-bold text-xs">
                  {user?.first_name ? user.first_name[0].toUpperCase() : <User className="h-4 w-4" />}
                </div>

                <Button
                  variant="ghost"
                  size="sm"
                  onClick={handleLogout}
                  className="h-8 px-2 text-xs text-slate-500 hover:text-red-600 dark:hover:text-red-400 flex items-center space-x-1"
                >
                  <LogOut className="h-3.5 w-3.5" />
                  <span className="hidden sm:inline">Logout</span>
                </Button>
              </div>
            ) : (
              <div className="flex items-center space-x-2">
                <Link to="/login">
                  <Button variant="ghost" size="sm" className="text-xs font-semibold">
                    Sign In
                  </Button>
                </Link>
                <Link to="/register">
                  <Button size="sm" className="bg-teal-700 hover:bg-teal-800 text-white text-xs font-semibold">
                    Register Institution
                  </Button>
                </Link>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <Outlet />
      </main>

      {/* System Footer */}
      <footer className="border-t border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 py-5">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 space-y-2 sm:space-y-0">
          <div className="flex items-center space-x-2">
            <ShieldCheck className="h-4 w-4 text-teal-600" />
            <span>&copy; {new Date().getFullYear()} Darsentra ERP &bull; Multi-Tenant K-12 School Management System</span>
          </div>
          <div className="flex items-center space-x-2 text-[11px]">
            <span>Islamabad / BISE / Cambridge Curricula</span>
            <span>&bull;</span>
            <Link to="/system-status" className="hover:underline text-teal-600">
              System Telemetry
            </Link>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default RootLayout;
