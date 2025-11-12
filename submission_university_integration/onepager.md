# One-page brief — University Data Integration

Objective: Centralize student, faculty, course and library data to reduce redundancy, enable real-time reporting, and simplify operations.

Key recommendation
- Build an ODS (Postgres) + MDM for golden records, with CDC ingestion where possible and a separate analytics warehouse (dbt-powered) for reporting.

Why it matters (3 quick benefits)
- Single source of truth: reduce time spent reconciling records and minimize administrative errors.
- Real-time visibility: enable enrollment and capacity dashboards to support academic planning and rapid decision-making.
- Stronger governance and security: consistent enforcement of privacy, access controls, and audit trails.

Phased approach (summary)
1. Discovery (2–4 weeks)
2. Pilot ODS + MDM (6–8 weeks) — SIS + one other system
3. Incremental rollout (8–16 weeks)
4. Cutover & stabilize (4–8 weeks)

Quick wins to deliver in pilot
- Real-time enrollment dashboard for two departments
- Faculty load report (sections per instructor)
- Data quality dashboard (duplicate rate, missing PII)

Ask from leadership
- Sponsor for Governance Board
- Access to SIS and HR system credentials for CDC or API integration
- Small pilot budget for 3 months (2–3 engineers + steward)

