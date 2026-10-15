import apiClient from "./api";
import type { ApiResponse } from "@/types/api";
import type {
  ActiveSchoolData,
  CurrentUserResponseData,
  LoginResponseData,
  SchoolSetupPayload,
} from "@/types/auth";
import type { School } from "@/types/school";

export interface RegisterPayload {
  email: string;
  password: string;
  password_confirm: string;
  first_name: string;
  last_name: string;
  phone_number?: string;
  cnic?: string;
}

export const authService = {
  async login(credentials: { email: string; password: string }): Promise<LoginResponseData> {
    const response = await apiClient.post<any>(
      "/api/v1/accounts/token/",
      credentials
    );
    return response.data?.data || response.data;
  },

  async register(data: RegisterPayload): Promise<LoginResponseData> {
    const response = await apiClient.post<any>(
      "/api/v1/accounts/register/",
      data
    );
    return response.data?.data || response.data;
  },

  async getCurrentUser(): Promise<CurrentUserResponseData> {
    const response = await apiClient.get<ApiResponse<CurrentUserResponseData>>(
      "/api/v1/accounts/me/"
    );
    return response.data.data!;
  },

  async getActiveSchool(): Promise<ActiveSchoolData> {
    const response = await apiClient.get<ApiResponse<ActiveSchoolData>>(
      "/api/v1/schools/active/"
    );
    return response.data.data!;
  },

  async setupSchool(payload: SchoolSetupPayload): Promise<School> {
    const response = await apiClient.post<ApiResponse<School>>(
      "/api/v1/schools/setup/",
      payload
    );
    return response.data.data!;
  },

  async getUserSchools(): Promise<School[]> {
    const response = await apiClient.get<ApiResponse<School[]>>(
      "/api/v1/schools/"
    );
    return response.data.data || [];
  },
};

export default authService;
