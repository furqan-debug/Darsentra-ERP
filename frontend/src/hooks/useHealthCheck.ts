import { useState, useEffect, useCallback } from "react";
import { healthService } from "@/services/healthService";
import type { HealthResponse } from "@/types/api";

interface HealthState {
  data: HealthResponse | null;
  isLoading: boolean;
  error: string | null;
  latencyMs: number | null;
  lastChecked: Date | null;
}

export function useHealthCheck(pollIntervalMs?: number) {
  const [state, setState] = useState<HealthState>({
    data: null,
    isLoading: true,
    error: null,
    latencyMs: null,
    lastChecked: null,
  });

  const check = useCallback(async () => {
    setState((prev) => ({ ...prev, isLoading: true, error: null }));
    const startTime = performance.now();

    try {
      const data = await healthService.checkHealth();
      const endTime = performance.now();
      setState({
        data,
        isLoading: false,
        error: null,
        latencyMs: Math.round(endTime - startTime),
        lastChecked: new Date(),
      });
    } catch (err: unknown) {
      const endTime = performance.now();
      const errorMessage =
        err instanceof Error
          ? err.message
          : typeof err === "object" && err !== null && "message" in err
          ? String((err as { message: unknown }).message)
          : "Failed to connect to backend server";

      setState({
        data: null,
        isLoading: false,
        error: errorMessage,
        latencyMs: Math.round(endTime - startTime),
        lastChecked: new Date(),
      });
    }
  }, []);

  useEffect(() => {
    check();

    if (pollIntervalMs && pollIntervalMs > 0) {
      const timer = setInterval(check, pollIntervalMs);
      return () => clearInterval(timer);
    }
  }, [check, pollIntervalMs]);

  return {
    ...state,
    refetch: check,
  };
}
