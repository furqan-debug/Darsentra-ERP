import apiClient from "./api";
import type { ApiResponse } from "@/types/api";
import type { AcademicClass, Section, Subject, AcademicYear } from "@/types/academics";

export interface CreateClassPayload {
  name: string;
  code?: string;
  order?: number;
}

export interface CreateSectionPayload {
  academic_class: string;
  name: string;
  room_number?: string;
  capacity?: number;
}

export const academicsService = {
  async getClasses(): Promise<AcademicClass[]> {
    const response = await apiClient.get<ApiResponse<AcademicClass[]>>(
      "/api/v1/academics/classes/"
    );
    return response.data.data || [];
  },

  async createClass(payload: CreateClassPayload): Promise<AcademicClass> {
    const response = await apiClient.post<ApiResponse<AcademicClass>>(
      "/api/v1/academics/classes/",
      payload
    );
    return response.data.data!;
  },

  async getSections(classId?: string): Promise<Section[]> {
    const params = classId ? { class_id: classId } : {};
    const response = await apiClient.get<ApiResponse<Section[]>>(
      "/api/v1/academics/sections/",
      { params }
    );
    return response.data.data || [];
  },

  async createSection(payload: CreateSectionPayload): Promise<Section> {
    const response = await apiClient.post<ApiResponse<Section>>(
      "/api/v1/academics/sections/",
      payload
    );
    return response.data.data!;
  },

  async getSubjects(): Promise<Subject[]> {
    const response = await apiClient.get<ApiResponse<Subject[]>>(
      "/api/v1/academics/subjects/"
    );
    return response.data.data || [];
  },

  async getAcademicYears(): Promise<AcademicYear[]> {
    const response = await apiClient.get<ApiResponse<AcademicYear[]>>(
      "/api/v1/academics/years/"
    );
    return response.data.data || [];
  },
};

export default academicsService;
