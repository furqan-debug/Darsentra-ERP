import React from "react";
import {
  Server,
  Database,
  RefreshCw,
  CheckCircle2,
  XCircle,
  Clock,
  Shield,
  Layers,
  Building2,
  Users,
  GraduationCap,
  CalendarCheck,
  FileCheck2,
  Receipt,
  UserCheck,
  BarChart3,
} from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { useHealthCheck } from "@/hooks/useHealthCheck";

export const App: React.FC = () => {
  const { data: health, isLoading, error, latencyMs, lastChecked, refetch } = useHealthCheck();

  const isHealthy = health?.status === "healthy" && health.database.status === "connected";

  const modules = [
    { name: "Accounts & Auth", icon: Users, status: "Ready (Custom User Model)", phase: "Foundation" },
    { name: "Schools / Tenants", icon: Building2, status: "Ready (Multi-Tenant RBAC)", phase: "Foundation" },
    { name: "Core & Health", icon: Server, status: "Active (/api/v1/health/)", phase: "Foundation" },
    { name: "Students", icon: GraduationCap, status: "Skeleton Prepared", phase: "Phase 2" },
    { name: "Academics", icon: Layers, status: "Skeleton Prepared", phase: "Phase 2" },
    { name: "Attendance", icon: CalendarCheck, status: "Skeleton Prepared", phase: "Phase 2" },
    { name: "Examinations", icon: FileCheck2, status: "Skeleton Prepared", phase: "Phase 2" },
    { name: "Fees & Finance", icon: Receipt, status: "Skeleton Prepared", phase: "Phase 2" },
    { name: "Staff & Faculty", icon: UserCheck, status: "Skeleton Prepared", phase: "Phase 2" },
    { name: "Reports & Analytics", icon: BarChart3, status: "Skeleton Prepared", phase: "Phase 2" },
  ];

  return (
    <div className="space-y-8">
      {/* Hero Section */}
      <div className="text-center space-y-3 max-w-3xl mx-auto pt-4">
        <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-teal-50 border border-teal-200 text-teal-800 text-xs font-medium dark:bg-teal-950 dark:border-teal-800 dark:text-teal-300">
          <Shield className="h-3.5 w-3.5 text-teal-600 dark:text-teal-400" />
          <span>Foundation Stage &bull; Pakistani K-12 School Management Suite</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-slate-900 dark:text-white">
          Darsentra ERP
        </h1>
        <p className="text-base sm:text-lg text-slate-600 dark:text-slate-400">
          A secure, modular, multi-tenant School Management SaaS platform engineered from scratch for Pakistani schools.
        </p>
      </div>

      {/* Backend Live Connection Status Card */}
      <Card className="border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden">
        <CardHeader className="bg-slate-50/50 dark:bg-slate-900/50 border-b border-slate-100 dark:border-slate-800 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center space-x-2">
              <Server className="h-5 w-5 text-teal-700 dark:text-teal-500" />
              <CardTitle>Backend & Database Connectivity</CardTitle>
            </div>
            <CardDescription>
              Real-time connectivity monitoring querying the backend health endpoint (<code className="text-xs bg-slate-100 dark:bg-slate-800 px-1.5 py-0.5 rounded">/api/v1/health/</code>)
            </CardDescription>
          </div>
          <Button
            variant="outline"
            size="sm"
            onClick={() => refetch()}
            disabled={isLoading}
            className="flex items-center space-x-1.5 shrink-0"
          >
            <RefreshCw className={`h-3.5 w-3.5 ${isLoading ? "animate-spin" : ""}`} />
            <span>Check Connectivity</span>
          </Button>
        </CardHeader>
        <CardContent className="pt-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Status Indicator */}
            <div className="flex items-center space-x-4 p-4 rounded-lg bg-slate-50 dark:bg-slate-900 border border-slate-100 dark:border-slate-800">
              {isLoading ? (
                <div className="h-10 w-10 rounded-full border-2 border-teal-600 border-t-transparent animate-spin shrink-0" />
              ) : isHealthy ? (
                <div className="h-10 w-10 rounded-full bg-emerald-100 dark:bg-emerald-950/60 text-emerald-600 dark:text-emerald-400 flex items-center justify-center shrink-0">
                  <CheckCircle2 className="h-6 w-6" />
                </div>
              ) : (
                <div className="h-10 w-10 rounded-full bg-red-100 dark:bg-red-950/60 text-red-600 dark:text-red-400 flex items-center justify-center shrink-0">
                  <XCircle className="h-6 w-6" />
                </div>
              )}
              <div className="space-y-1">
                <span className="text-xs font-medium text-slate-500 dark:text-slate-400">Application State</span>
                <div>
                  {isLoading ? (
                    <Badge variant="outline" className="animate-pulse">Checking...</Badge>
                  ) : isHealthy ? (
                    <Badge variant="success">Connected &bull; Healthy</Badge>
                  ) : (
                    <Badge variant="destructive">Disconnected</Badge>
                  )}
                </div>
              </div>
            </div>

            {/* Database Engine Indicator */}
            <div className="flex items-center space-x-4 p-4 rounded-lg bg-slate-50 dark:bg-slate-900 border border-slate-100 dark:border-slate-800">
              <div className="h-10 w-10 rounded-full bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 flex items-center justify-center shrink-0">
                <Database className="h-5 w-5" />
              </div>
              <div className="space-y-1">
                <span className="text-xs font-medium text-slate-500 dark:text-slate-400">Database Connection</span>
                <div className="text-sm font-semibold capitalize text-slate-900 dark:text-white">
                  {isLoading
                    ? "Verifying..."
                    : isHealthy
                    ? `${health?.database.status} (${health?.database.engine})`
                    : "Unreachable"}
                </div>
              </div>
            </div>

            {/* Ping & Telemetry */}
            <div className="flex items-center space-x-4 p-4 rounded-lg bg-slate-50 dark:bg-slate-900 border border-slate-100 dark:border-slate-800">
              <div className="h-10 w-10 rounded-full bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 flex items-center justify-center shrink-0">
                <Clock className="h-5 w-5" />
              </div>
              <div className="space-y-1">
                <span className="text-xs font-medium text-slate-500 dark:text-slate-400">Round-Trip Latency</span>
                <div className="text-sm font-semibold text-slate-900 dark:text-white">
                  {isLoading ? "Measuring..." : latencyMs !== null ? `${latencyMs} ms` : "N/A"}
                </div>
              </div>
            </div>
          </div>

          {/* Error Message Details if any */}
          {error && (
            <div className="mt-4 p-4 rounded-md bg-red-50 dark:bg-red-950/40 border border-red-200 dark:border-red-900/60 text-xs text-red-800 dark:text-red-300">
              <p className="font-semibold mb-1">Backend Connection Notice:</p>
              <p>{error}</p>
              <p className="mt-1 text-[11px] text-red-600 dark:text-red-400">
                Ensure the Django backend is running (<code className="bg-red-100 dark:bg-red-900/40 px-1 py-0.5 rounded">python manage.py runserver</code> or via Docker Compose) and reachable at <code className="bg-red-100 dark:bg-red-900/40 px-1 py-0.5 rounded">http://localhost:8000</code>.
              </p>
            </div>
          )}

          {lastChecked && (
            <div className="mt-4 text-right text-[11px] text-slate-400">
              Last checked: {lastChecked.toLocaleTimeString()}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Architecture Foundations Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="border-slate-200 dark:border-slate-800">
          <CardHeader>
            <div className="h-8 w-8 rounded-md bg-teal-100 dark:bg-teal-900/50 text-teal-800 dark:text-teal-300 flex items-center justify-center mb-2">
              <Shield className="h-4 w-4" />
            </div>
            <CardTitle className="text-base">Multi-Tenant Isolation</CardTitle>
            <CardDescription className="text-xs">
              Row-level tenant scoping anchored by School and SchoolMembership models. Client-provided tenant IDs are never trusted blindly.
            </CardDescription>
          </CardHeader>
        </Card>

        <Card className="border-slate-200 dark:border-slate-800">
          <CardHeader>
            <div className="h-8 w-8 rounded-md bg-teal-100 dark:bg-teal-900/50 text-teal-800 dark:text-teal-300 flex items-center justify-center mb-2">
              <Users className="h-4 w-4" />
            </div>
            <CardTitle className="text-base">Custom User & RBAC</CardTitle>
            <CardDescription className="text-xs">
              UUID-based custom User model with email authentication, Pakistani CNIC/phone fields, and roles (Owner, Principal, Teacher, Accountant, etc.).
            </CardDescription>
          </CardHeader>
        </Card>

        <Card className="border-slate-200 dark:border-slate-800">
          <CardHeader>
            <div className="h-8 w-8 rounded-md bg-teal-100 dark:bg-teal-900/50 text-teal-800 dark:text-teal-300 flex items-center justify-center mb-2">
              <Layers className="h-4 w-4" />
            </div>
            <CardTitle className="text-base">Modular Architecture</CardTitle>
            <CardDescription className="text-xs">
              Clean separation of models, serializers, views, services, permissions, and REST routes across all 10 domain applications.
            </CardDescription>
          </CardHeader>
        </Card>
      </div>

      {/* Modular Applications Registry */}
      <Card className="border-slate-200 dark:border-slate-800">
        <CardHeader>
          <CardTitle className="text-base">System Modules Status</CardTitle>
          <CardDescription className="text-xs">
            Architectural inventory of backend modules established for the Darsentra ERP platform.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
            {modules.map((mod) => {
              const Icon = mod.icon;
              return (
                <div
                  key={mod.name}
                  className="p-3 rounded-lg border border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-900/50 space-y-1.5"
                >
                  <div className="flex items-center justify-between">
                    <Icon className="h-4 w-4 text-teal-700 dark:text-teal-500" />
                    <Badge variant={mod.phase === "Foundation" ? "success" : "secondary"} className="text-[10px]">
                      {mod.phase}
                    </Badge>
                  </div>
                  <div className="font-medium text-xs text-slate-900 dark:text-white truncate">{mod.name}</div>
                  <div className="text-[11px] text-slate-500 dark:text-slate-400">{mod.status}</div>
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default App;
