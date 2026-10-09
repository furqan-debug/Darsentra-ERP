import React from "react";
import { Link, Outlet } from "react-router-dom";
import { School, ShieldCheck, Database, Layers } from "lucide-react";
import { Badge } from "@/components/ui/badge";

export const RootLayout: React.FC = () => {
  return (
    <div className="min-h-screen flex flex-col bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100">
      {/* Top Navigation Bar */}
      <header className="sticky top-0 z-40 w-full border-b border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="h-10 w-10 rounded-lg bg-teal-700 dark:bg-teal-600 flex items-center justify-center text-white shadow-sm">
              <School className="h-5 w-5" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <Link to="/" className="text-xl font-bold tracking-tight text-slate-900 dark:text-white">
                  Darsentra ERP
                </Link>
                <Badge variant="outline" className="text-[11px] font-mono border-teal-600 text-teal-700 dark:text-teal-400">
                  Foundation v1.0
                </Badge>
              </div>
              <p className="text-xs text-slate-500 dark:text-slate-400">
                School Management SaaS for Pakistan K-12
              </p>
            </div>
          </div>

          <div className="hidden sm:flex items-center space-x-4 text-xs text-slate-600 dark:text-slate-300">
            <div className="flex items-center space-x-1">
              <ShieldCheck className="h-4 w-4 text-teal-600" />
              <span>Multi-Tenant Row Isolation</span>
            </div>
            <div className="flex items-center space-x-1">
              <Database className="h-4 w-4 text-teal-600" />
              <span>PostgreSQL 16</span>
            </div>
            <div className="flex items-center space-x-1">
              <Layers className="h-4 w-4 text-teal-600" />
              <span>Modular Monolith</span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Outlet />
      </main>

      {/* System Footer */}
      <footer className="border-t border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 space-y-2 sm:space-y-0">
          <div>
            &copy; {new Date().getFullYear()} Darsentra ERP. All rights reserved. Built for Pakistani educational institutions.
          </div>
          <div className="flex items-center space-x-3">
            <span>Django REST Framework</span>
            <span>&bull;</span>
            <span>React + TypeScript + Vite</span>
            <span>&bull;</span>
            <span>Tailwind CSS</span>
          </div>
        </div>
      </footer>
    </div>
  );
};
