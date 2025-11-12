# University Data Integration Plan

## Executive summary
A large university currently operates siloed systems for student information, faculty records, course management and library services. This plan delivers a practical, phased approach to build a centralized Operational Data Store (ODS) with Master Data Management (MDM) to produce golden records, plus an analytics warehouse for reporting and dashboards. The design emphasizes near‑real‑time ingestion (CDC where possible), strong security and governance, and an incremental rollout that minimizes risk while delivering early value.

Deliverables in this submission
- Architecture and recommended stack
- Canonical data model and sample SQL DDLs (see `sql/ddl_core_tables.sql`)
- Integration & migration plan (phased)
- Security & governance plan
- Implementation timeline, KPIs and next steps
- ER diagram (PlantUML): `er_diagram.puml`

---

## 1. High-level architecture
- Source systems: SIS (Student Information System), HR/faculty system, LMS/CMS, Library system.
- Integration layer: CDC (Debezium) for source DBs → message bus (Kafka or managed equivalent). For SaaS or non‑DB sources, use API adapters or batch ETL (Airbyte, custom ETL via Airflow).
- ODS (canonical database): PostgreSQL (managed RDS/Aurora or Azure Database) storing canonical entities and golden records.
- MDM layer: deterministic + probabilistic matching to create and maintain golden records, with a stewardship UI for human review.
- Analytics data warehouse: Snowflake / BigQuery / Redshift or a scalable OLAP solution; use dbt for transformations and lineage.
- API layer: read APIs for apps and dashboards, with an API gateway and RBAC.
- Governance & catalog: Data catalog (DataHub/Amundsen), Data Stewards and a Data Governance Board.

Principles: idempotent upserts to ODS, preserve provenance, phased rollout, start with deterministic matching and iterate.

---

## 2. Canonical data model (conceptual)
Core entities and relationships (high-level):
- Student (1) —< Enrollment >— (M) Section/CourseInstance (M) — (1) Course
- Faculty (1) —< Section (instructor) (M)
- LibraryRecord linked to Student or Faculty
- Department and Program entities referenced by Course, Faculty, and Student program

Key attributes (examples):
- Student: student_id (uuid), sis_student_number, national_id, name, dob, primary_email, phone, enrollment_status, metadata (jsonb), created_at, updated_at
- Faculty: faculty_id, hr_employee_id, name, title, department_id, email, hire_date, status
- Course: course_id, course_code, title, credits, department_id
- Section: section_id, course_id, term, year, capacity, instructor_faculty_id, schedule
- Enrollment: enrollment_id, student_id, section_id, status, grade, enrolled_at
- LibraryRecord: record_id, borrower_id (student or faculty), item_id, loan_date, due_date, returned_date, fines

Refer to `sql/ddl_core_tables.sql` for full CREATE TABLE statements and indexes.

---

## 3. Integration & migration plan (phased)
Phase 0 — Discovery (2–4 weeks)
- Inventory all source systems, schemas, owners and data volumes.
- Identify deterministic keys (national ID, institutional IDs) and assess data quality.
- Choose initial pilot cohort (e.g., last 2 years of enrollments or one faculty group).

Phase 1 — Pilot & canonical model (6–8 weeks)
- Spin up ODS (Postgres) and create pilot schema: student, faculty, course, section, enrollment.
- Build connectors for the most critical systems (SIS and HR or SIS and LMS).
- Implement basic MDM rules: deterministic merge on institutional ID or national ID; probabilistic matching for others with a stewardship queue.
- Build 3–4 dashboards demonstrating value (enrollment by course, faculty load, course fill rate).

Phase 2 — Incremental rollout (8–16 weeks)
- Add remaining systems (library, other course/campus systems), extend MDM rules, harden monitoring and alerts.
- Implement CDC across supported sources, fallback to scheduled ETL or API polling where needed.
- Introduce API gateway & begin migrating apps to read from canonical APIs.

Phase 3 — Cutover & decommission (4–8 weeks)
- Run dual-read/dual-write strategies for critical systems as needed.
- Migrate reporting and downstream systems to use canonical APIs/warehouse.
- Decommission or restrict writes to legacy stores once confidence is achieved.

Phase 4 — Stabilize & operate (ongoing)
- Continuous quality monitoring, governance, and dataset onboarding.
- Iterate on matching rules and steward backlog.

Rollout approach: conservative pilot → demonstrate ROI → expand by data domain.

---

## 4. Security, privacy & compliance
- Authentication: SSO via SAML/OAuth2 (Azure AD/Keycloak). Use MFA for admin/steward accounts.
- Authorization: RBAC at API layer; column-level masking for sensitive PII in analytics views.
- Encryption: TLS in transit; at-rest encryption for database storage; consider field-level encryption for national IDs.
- Audit & logging: append-only audit topics (Kafka) and database audit tables; retain logs according to policy.
- Backups & DR: point-in-time recovery enabled; periodic DR exercises.
- Compliance mapping: FERPA-like controls, GDPR where applicable; data retention and deletion workflows.

---

## 5. Data governance & operational processes
- Data Governance Board with representatives from Registrar, HR, Library, IT, and Faculty.
- Data Stewards assigned per domain, empowered to resolve steward queue items and approve schema changes.
- Data catalog (DataHub/Amundsen) for discoverability and data lineage.
- SLAs: specify freshness expectations (e.g., SIS updates within 1–5 minutes via CDC; library sync hourly).
- Reconciliation jobs and anomaly detection for data drift and duplicate increases.

---

## 6. KPIs and reports (quick wins)
- Real-time enrollments by course/section and current fill rates.
- Faculty teaching load per term (sections, contact hours).
- Course utilization and capacity alerts (>95% fill rate).
- Library overdue items and fines by borrower segment.
- Data quality metrics: duplicate rate, missing key fields, reconciliation pass rate.

---

## 7. Implementation timeline and resourcing (high level)
- Pilot: 2–3 engineers + 1 data steward + part-time product owner — 2–3 months.
- Full rollout: 3–6 engineers, 1–2 stewards, governance board — 4–6 additional months.
- Ongoing operations: 1–2 data engineers, part-time stewarding.

---

## 8. Risks & mitigations
- Poor source data quality: prioritize deterministic matching and stewarding; run focused data-cleaning sprints.
- Institutional resistance: engage stakeholders early, deliver quick dashboards that show time and cost savings.
- Security incidents: hardened access controls, periodic audits, least-privilege access.
- Cost overrun: phased approach, prefer managed cloud services to minimize ops.
