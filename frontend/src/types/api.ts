export interface DatabaseHealth {
  status: "connected" | "disconnected";
  engine?: string;
  error?: string | null;
}

export interface HealthResponse {
  status: "healthy" | "unhealthy";
  service: string;
  version: string;
  environment: string;
  database: DatabaseHealth;
  timestamp: string;
}

export interface ApiResponse<T> {
  status: "success" | "error";
  data?: T;
  message?: string;
  code?: string;
  errors?: Record<string, unknown> | string[];
}
