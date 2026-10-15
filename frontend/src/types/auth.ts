import { School, SchoolMembership } from "./school";

export interface UserSummary {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  full_name: string;
  phone_number?: string;
  cnic?: string;
  is_staff: boolean;
  is_superuser: boolean;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface SchoolSummary {
  id: string;
  name: string;
  code: string;
  slug: string;
  curriculum_type: string;
  curriculum_display?: string;
  city: string;
  province: string;
  role: string;
  role_display: string;
}

export interface LoginResponseData {
  access: string;
  refresh: string;
  user: UserSummary;
  schools?: SchoolSummary[];
  active_school?: SchoolSummary | null;
  memberships?: SchoolMembership[];
}

export interface CurrentUserResponseData {
  user: UserSummary;
  schools: SchoolSummary[];
  active_school: SchoolSummary | null;
}

export interface ActiveSchoolStats {
  total_students: number;
  total_staff: number;
  total_classes: number;
  total_sections: number;
  active_session: string;
}

export interface ActiveSchoolData {
  has_school: boolean;
  school: School | null;
  role?: string;
  role_display?: string;
  stats?: ActiveSchoolStats | null;
}

export interface SchoolSetupPayload {
  name: string;
  code: string;
  registration_number?: string;
  curriculum_type: string;
  contact_email?: string;
  phone_number?: string;
  address?: string;
  city?: string;
  province?: string;
  academic_year_name?: string;
  initial_classes?: string[];
}
