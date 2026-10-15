import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import { RootLayout } from "./layouts/RootLayout";
import { ProtectedRoute } from "./components/ProtectedRoute";
import { PublicOnlyRoute } from "./components/PublicOnlyRoute";
import { LoginPage } from "./features/accounts/LoginPage";
import { RegisterPage } from "./features/accounts/RegisterPage";
import { SchoolSetupWizard } from "./features/schools/SchoolSetupWizard";
import { DashboardPage } from "./features/schools/DashboardPage";
import App from "./App";
import "./index.css";

const IndexRouteRedirect: React.FC = () => {
  const { isAuthenticated, hasSchool, isLoading } = useAuth();
  if (isLoading) return null;
  if (isAuthenticated) {
    if (hasSchool) {
      return <Navigate to="/dashboard" replace />;
    }
    return <Navigate to="/setup-school" replace />;
  }
  return <Navigate to="/login" replace />;
};

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<RootLayout />}>
            {/* Root index redirect based on auth status */}
            <Route index element={<IndexRouteRedirect />} />

            {/* Public Only (Unauthenticated) Routes */}
            <Route element={<PublicOnlyRoute />}>
              <Route path="login" element={<LoginPage />} />
              <Route path="register" element={<RegisterPage />} />
            </Route>

            {/* Protected Routes (Authentication Required) */}
            <Route element={<ProtectedRoute />}>
              <Route path="dashboard" element={<DashboardPage />} />
              <Route path="setup-school" element={<SchoolSetupWizard />} />
            </Route>

            {/* System Telemetry & Health Page */}
            <Route path="system-status" element={<App />} />

            {/* Catch-all redirect */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Route>
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>
);
