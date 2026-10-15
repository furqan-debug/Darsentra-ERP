import React, { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { Building2, KeyRound, Lock, LogIn, Mail, ShieldCheck } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { useAuth } from "@/context/AuthContext";

export const LoginPage: React.FC = () => {
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const from = (location.state as { from?: { pathname: string } })?.from?.pathname || "/dashboard";

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage(null);
    setIsLoading(true);

    try {
      const data = await login({ email, password });
      if (
        data.active_school ||
        (data.schools && data.schools.length > 0) ||
        (data.memberships && data.memberships.length > 0)
      ) {
        navigate(from, { replace: true });
      } else {
        navigate("/setup-school", { replace: true });
      }
    } catch (err: any) {
      if (err?.errors?.detail) {
        setErrorMessage(err.errors.detail);
      } else if (err?.message) {
        setErrorMessage(err.message);
      } else {
        setErrorMessage("Invalid credentials. Please verify your email and password.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleDemoFill = (demoEmail: string, demoPass: string) => {
    setEmail(demoEmail);
    setPassword(demoPass);
  };

  return (
    <div className="min-h-[75vh] flex items-center justify-center py-6 px-4">
      <div className="max-w-md w-full space-y-6">
        {/* Brand Header */}
        <div className="text-center space-y-2">
          <div className="inline-flex h-12 w-12 rounded-2xl bg-teal-700 text-white items-center justify-center shadow-lg shadow-teal-700/20">
            <Building2 className="h-6 w-6" />
          </div>
          <h2 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-slate-900 dark:text-white">
            Welcome to Darsentra
          </h2>
          <p className="text-sm text-slate-600 dark:text-slate-400">
            Sign in to access your school workspace and administrative dashboard
          </p>
        </div>

        {/* Login Form Card */}
        <Card className="border-slate-200 dark:border-slate-800 shadow-md">
          <CardHeader className="space-y-1 pb-4">
            <CardTitle className="text-lg">Sign In</CardTitle>
            <CardDescription className="text-xs">
              Enter your official email and password to proceed
            </CardDescription>
          </CardHeader>
          <CardContent>
            {errorMessage && (
              <div className="mb-4 p-3 rounded-md bg-red-50 dark:bg-red-950/40 border border-red-200 dark:border-red-900 text-xs text-red-700 dark:text-red-300">
                {errorMessage}
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-1.5">
                <label className="text-xs font-semibold text-slate-700 dark:text-slate-300">
                  Email Address
                </label>
                <div className="relative">
                  <Mail className="absolute left-3 top-2.5 h-4 w-4 text-slate-400" />
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="e.g. principal@school.edu.pk"
                    className="w-full pl-9 pr-3 py-2 text-sm rounded-md border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-teal-600"
                  />
                </div>
              </div>

              <div className="space-y-1.5">
                <div className="flex items-center justify-between">
                  <label className="text-xs font-semibold text-slate-700 dark:text-slate-300">
                    Password
                  </label>
                </div>
                <div className="relative">
                  <Lock className="absolute left-3 top-2.5 h-4 w-4 text-slate-400" />
                  <input
                    type="password"
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="••••••••••••"
                    className="w-full pl-9 pr-3 py-2 text-sm rounded-md border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-teal-600"
                  />
                </div>
              </div>

              <Button
                type="submit"
                disabled={isLoading}
                className="w-full bg-teal-700 hover:bg-teal-800 text-white font-medium flex items-center justify-center space-x-2 py-2.5"
              >
                {isLoading ? (
                  <div className="h-4 w-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                ) : (
                  <>
                    <LogIn className="h-4 w-4" />
                    <span>Sign In to Dashboard</span>
                  </>
                )}
              </Button>
            </form>

            {/* Quick Demo Pre-Fill */}
            <div className="mt-5 pt-4 border-t border-slate-100 dark:border-slate-800">
              <p className="text-[11px] font-medium text-slate-500 mb-2 flex items-center space-x-1">
                <KeyRound className="h-3 w-3 text-teal-600" />
                <span>Quick Seeded Accounts:</span>
              </p>
              <div className="grid grid-cols-1 gap-1.5">
                <button
                  type="button"
                  onClick={() => handleDemoFill("admin@darsentra.pk", "Admin1234!")}
                  className="text-left text-xs p-2 rounded bg-slate-50 dark:bg-slate-800 hover:bg-teal-50 dark:hover:bg-slate-700 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-200 transition-colors"
                >
                  <span className="font-semibold text-teal-700 dark:text-teal-400">School Owner:</span> admin@darsentra.pk / Admin1234!
                </button>
              </div>
            </div>

            <div className="mt-4 text-center">
              <p className="text-xs text-slate-500">
                New school founder?{" "}
                <Link
                  to="/register"
                  className="font-semibold text-teal-700 hover:text-teal-800 dark:text-teal-400"
                >
                  Register institution
                </Link>
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Security Feature Notice */}
        <div className="flex items-center justify-center space-x-2 text-xs text-slate-500">
          <ShieldCheck className="h-4 w-4 text-teal-600" />
          <span>Protected by strict row-level multi-tenant isolation</span>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
