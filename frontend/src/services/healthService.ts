import apiClient from "./api";
import type { HealthResponse } from "@/types/api";

export const healthService = {
  /**
   * Fetches the current health and database status from /api/v1/health/
   */
  async checkHealth(): Promise<HealthResponse> {
    const response = await apiClient.get<HealthResponse>("/api/v1/health/");
    return response.data;
  },
};
