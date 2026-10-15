export interface Section {
  id: string;
  name: string;
  room_number?: string;
  capacity: number;
  created_at: string;
}

export interface AcademicClass {
  id: string;
  name: string;
  code?: string;
  order: number;
  sections: Section[];
  section_count: number;
  created_at: string;
}

export interface Subject {
  id: string;
  name: string;
  code?: string;
  is_elective: boolean;
  created_at: string;
}

export interface AcademicYear {
  id: string;
  name: string;
  start_date?: string;
  end_date?: string;
  is_current: boolean;
  created_at: string;
}
