export type MembershipRole =
  | "owner"
  | "principal"
  | "admin"
  | "teacher"
  | "accountant"
  | "student"
  | "parent"
  | "staff";

export interface School {
  id: string;
  name: string;
  slug: string;
  code: string;
  registration_number?: string;
  curriculum_type: string;
  curriculum_display?: string;
  contact_email?: string;
  phone_number?: string;
  address?: string;
  city: string;
  province: string;
  province_display?: string;
  is_active: boolean;
  created_at: string;
}

export interface SchoolMembership {
  id: string;
  school: School;
  role: MembershipRole;
  role_display: string;
  is_active: boolean;
  created_at: string;
}
