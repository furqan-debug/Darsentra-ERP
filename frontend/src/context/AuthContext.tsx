import React, {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
} from "react";
import authService, { RegisterPayload } from "@/services/authService";
import type {
  ActiveSchoolStats,
  LoginResponseData,
  UserSummary,
} from "@/types/auth";
import type { School } from "@/types/school";

interface AuthContextType {
  user: UserSummary | null;
  token: string | null;
  activeSchool: School | null;
  activeRole: string | null;
  activeRoleDisplay: string | null;
  schoolStats: ActiveSchoolStats | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  hasSchool: boolean;
  login: (credentials: { email: string; password: string }) => Promise<LoginResponseData>;
  register: (payload: RegisterPayload) => Promise<LoginResponseData>;
  logout: () => void;
  switchSchool: (schoolId: string) => Promise<void>;
  refreshActiveSchool: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<UserSummary | null>(null);
  const [token, setToken] = useState<string | null>(() => localStorage.getItem("darsentra_access_token"));
  const [activeSchool, setActiveSchool] = useState<School | null>(null);
  const [activeRole, setActiveRole] = useState<string | null>(null);
  const [activeRoleDisplay, setActiveRoleDisplay] = useState<string | null>(null);
  const [schoolStats, setSchoolStats] = useState<ActiveSchoolStats | null>(null);
  const [hasSchool, setHasSchool] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  const refreshActiveSchool = useCallback(async () => {
    try {
      const activeData = await authService.getActiveSchool();
      setHasSchool(activeData.has_school);
      setActiveSchool(activeData.school || null);
      if (activeData.role) setActiveRole(activeData.role);
      if (activeData.role_display) setActiveRoleDisplay(activeData.role_display);
      setSchoolStats(activeData.stats || null);
      if (activeData.school?.id) {
        localStorage.setItem("darsentra_active_school_id", activeData.school.id);
      } else {
        localStorage.removeItem("darsentra_active_school_id");
      }
    } catch {
      setActiveSchool(null);
      setHasSchool(false);
      setSchoolStats(null);
    }
  }, []);

  const bootstrapAuth = useCallback(async () => {
    const savedToken = localStorage.getItem("darsentra_access_token");
    if (!savedToken) {
      setUser(null);
      setActiveSchool(null);
      setIsLoading(false);
      return;
    }

    try {
      const meData = await authService.getCurrentUser();
      setUser(meData.user);
      if (meData.active_school) {
        setActiveRole(meData.active_school.role);
        setActiveRoleDisplay(meData.active_school.role_display);
      }
      await refreshActiveSchool();
    } catch {
      localStorage.removeItem("darsentra_access_token");
      localStorage.removeItem("darsentra_refresh_token");
      localStorage.removeItem("darsentra_active_school_id");
      setToken(null);
      setUser(null);
      setActiveSchool(null);
    } finally {
      setIsLoading(false);
    }
  }, [refreshActiveSchool]);

  useEffect(() => {
    bootstrapAuth();
  }, [bootstrapAuth]);

  const login = async (credentials: { email: string; password: string }): Promise<LoginResponseData> => {
    setIsLoading(true);
    try {
      const data = await authService.login(credentials);
      localStorage.setItem("darsentra_access_token", data.access);
      localStorage.setItem("darsentra_refresh_token", data.refresh);
      setToken(data.access);
      setUser(data.user);

      if (data.active_school) {
        localStorage.setItem("darsentra_active_school_id", data.active_school.id);
        setActiveRole(data.active_school.role);
        setActiveRoleDisplay(data.active_school.role_display);
        setHasSchool(true);
      } else if (data.schools && data.schools.length > 0) {
        const primary = data.schools[0];
        localStorage.setItem("darsentra_active_school_id", primary.id);
        setActiveRole(primary.role);
        setActiveRoleDisplay(primary.role_display);
        setHasSchool(true);
      }

      await refreshActiveSchool();
      return data;
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (payload: RegisterPayload): Promise<LoginResponseData> => {
    setIsLoading(true);
    try {
      const resp = await authService.register(payload);
      // If the register endpoint returned tokens directly, store them
      if (resp.access && resp.refresh) {
        localStorage.setItem("darsentra_access_token", resp.access);
        localStorage.setItem("darsentra_refresh_token", resp.refresh);
        setToken(resp.access);
        setUser(resp.user);
      } else {
        await login({ email: payload.email, password: payload.password });
      }
      return resp;
    } finally {
      setIsLoading(false);
    }
  };

  const switchSchool = async (schoolId: string) => {
    localStorage.setItem("darsentra_active_school_id", schoolId);
    await refreshActiveSchool();
  };

  const logout = () => {
    localStorage.removeItem("darsentra_access_token");
    localStorage.removeItem("darsentra_refresh_token");
    localStorage.removeItem("darsentra_active_school_id");
    setToken(null);
    setUser(null);
    setActiveSchool(null);
    setActiveRole(null);
    setActiveRoleDisplay(null);
    setSchoolStats(null);
    setHasSchool(false);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        activeSchool,
        activeRole,
        activeRoleDisplay,
        schoolStats,
        isLoading,
        isAuthenticated: !!token && !!user,
        hasSchool,
        login,
        register,
        logout,
        switchSchool,
        refreshActiveSchool,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
