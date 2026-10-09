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

// Interceptor to inject optional tenant header if active tenant is selected
apiClient.interceptors.request.use(
  (config) => {
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
    if (error.response?.data) {
      // Backend returned consistent error payload
      return Promise.reject(error.response.data);
    }
    return Promise.reject({
      status: "error",
      message: error.message || "Network error. Please verify backend connectivity.",
    });
  }
);

export default apiClient;
