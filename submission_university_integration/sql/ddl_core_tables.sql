-- SQL DDLs for core canonical tables (PostgreSQL)

CREATE SCHEMA IF NOT EXISTS canonical;

-- Students
CREATE TABLE IF NOT EXISTS canonical.student (
  student_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  sis_student_number TEXT,
  national_id TEXT,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  preferred_name TEXT,
  dob DATE,
  gender TEXT,
  primary_email TEXT,
  phone_number TEXT,
  address JSONB,
  enrollment_status TEXT,
  metadata JSONB,
  source_systems JSONB,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);
CREATE UNIQUE INDEX IF NOT EXISTS ux_student_national_id ON canonical.student (national_id) WHERE national_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS ix_student_email ON canonical.student (primary_email);

-- Faculty
CREATE TABLE IF NOT EXISTS canonical.faculty (
  faculty_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  hr_employee_id TEXT,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  title TEXT,
  department_id UUID,
  primary_email TEXT,
  phone_number TEXT,
  hire_date DATE,
  employment_status TEXT,
  metadata JSONB,
  source_systems JSONB,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX IF NOT EXISTS ix_faculty_email ON canonical.faculty (primary_email);

-- Department
CREATE TABLE IF NOT EXISTS canonical.department (
  department_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  code TEXT,
  name TEXT,
  metadata JSONB,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- Course
CREATE TABLE IF NOT EXISTS canonical.course (
  course_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  course_code TEXT NOT NULL,
  title TEXT NOT NULL,
  credits NUMERIC(4,2),
  department_id UUID,
  description TEXT,
  metadata JSONB,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);
CREATE UNIQUE INDEX IF NOT EXISTS ux_course_code ON canonical.course (course_code);

-- Section / CourseInstance
CREATE TABLE IF NOT EXISTS canonical.section (
  section_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  course_id UUID NOT NULL,
  term TEXT,
  year INTEGER,
  capacity INTEGER,
  instructor_faculty_id UUID,
  location TEXT,
  schedule JSONB,
  metadata JSONB,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now(),
  FOREIGN KEY (course_id) REFERENCES canonical.course(course_id),
  FOREIGN KEY (instructor_faculty_id) REFERENCES canonical.faculty(faculty_id)
);

-- Enrollment
CREATE TABLE IF NOT EXISTS canonical.enrollment (
  enrollment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  student_id UUID NOT NULL,
  section_id UUID NOT NULL,
  enrollment_status TEXT,
  grade TEXT,
  enrolled_at TIMESTAMPTZ DEFAULT now(),
  dropped_at TIMESTAMPTZ,
  metadata JSONB,
  source_systems JSONB,
  FOREIGN KEY (student_id) REFERENCES canonical.student(student_id),
  FOREIGN KEY (section_id) REFERENCES canonical.section(section_id)
);
CREATE INDEX IF NOT EXISTS ix_enrollment_student ON canonical.enrollment (student_id);
CREATE INDEX IF NOT EXISTS ix_enrollment_section ON canonical.enrollment (section_id);

-- Library records
CREATE TABLE IF NOT EXISTS canonical.library_record (
  record_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  borrower_id UUID NOT NULL,
  borrower_type TEXT CHECK (borrower_type IN ('student','faculty')),
  item_id TEXT,
  checkout_date TIMESTAMPTZ,
  due_date TIMESTAMPTZ,
  returned_date TIMESTAMPTZ,
  fines NUMERIC(10,2),
  metadata JSONB,
  source_systems JSONB
);

-- Basic triggers to maintain updated_at
CREATE OR REPLACE FUNCTION canonical.update_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$;

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'student_update_ts') THEN
    CREATE TRIGGER student_update_ts BEFORE UPDATE ON canonical.student FOR EACH ROW EXECUTE FUNCTION canonical.update_updated_at();
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'faculty_update_ts') THEN
    CREATE TRIGGER faculty_update_ts BEFORE UPDATE ON canonical.faculty FOR EACH ROW EXECUTE FUNCTION canonical.update_updated_at();
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'course_update_ts') THEN
    CREATE TRIGGER course_update_ts BEFORE UPDATE ON canonical.course FOR EACH ROW EXECUTE FUNCTION canonical.update_updated_at();
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'section_update_ts') THEN
    CREATE TRIGGER section_update_ts BEFORE UPDATE ON canonical.section FOR EACH ROW EXECUTE FUNCTION canonical.update_updated_at();
  END IF;
END;
$$;
