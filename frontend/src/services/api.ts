import axios, { type AxiosInstance, type AxiosError } from "axios";
import type { ApiResponse } from "@/types/api";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 10000,
});

// Interceptor to inject JWT token and active tenant header
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("darsentra_access_token");
    if (token && !config.headers["Authorization"]) {
      config.headers["Authorization"] = `Bearer ${token}`;
    }

    const activeSchoolId = localStorage.getItem("darsentra_active_school_id");
    if (activeSchoolId && !config.headers["X-School-ID"]) {
      config.headers["X-School-ID"] = activeSchoolId;
    }

    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor to handle standard API errors
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError<ApiResponse<unknown>>) => {
    if (error.response?.status === 401) {
      // Clear token if unauthorized on a protected endpoint
      const isAuthEndpoint = error.config?.url?.includes("/accounts/token/");
      if (!isAuthEndpoint) {
        localStorage.removeItem("darsentra_access_token");
        localStorage.removeItem("darsentra_refresh_token");
      }
    }

    if (error.response?.data) {
      return Promise.reject(error.response.data);
    }

    return Promise.reject({
      status: "error",
      message: error.message || "Network error. Please verify backend connectivity.",
    });
  }
);

export default apiClient;
